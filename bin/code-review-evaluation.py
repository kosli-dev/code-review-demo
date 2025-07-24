#! /usr/bin/env python3
import json
import sys
import requests
import argparse
from typing import List, Optional


def make_attestations_request(
    host: str,
    org: str,
    flow_name: Optional[str],
    commit_list: List[str],
    attestation_type: str,
    api_token: str,
) -> dict:
    """
    Make API request to list attestations for criteria.

    Args:
        host: The API host URL
        org: Organization name
        flow_name: Name of the flow (can be None)
        commit_list: List of commit SHAs
        attestation_type: Type of attestation to filter by
        api_token: API token for authorization

    Returns:
        JSON response from the API
    """
    url = f"{host}/api/v2/attestations/{org}/list_attestations_for_criteria"

    # Build query parameters
    params = {"attestation_type": attestation_type}

    # Only include flow_name if it's not None
    if flow_name is not None:
        params["flow_name"] = flow_name

    # Add commit_list parameters - use list to allow multiple values
    params["commit_list"] = commit_list

    headers = {"accept": "application/json", "Authorization": f"Bearer {api_token}"}

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}", file=sys.stderr)
        sys.exit(1)


def evaluate_attestation(commit_hash, attestation):
    result = {
        "commit": commit_hash,
        "pass": False,
        "reason": "",
        "attestation_url": attestation.get("html_url", ""),
        "pr_url": attestation.get("pull_requests", [])[0].get("url", ""),
    }

    att_type = attestation.get("attestation_type")
    is_compliant = attestation.get("is_compliant", False)

    if att_type == "override":
        if is_compliant:
            result["pass"] = True
            result["reason"] = "Overridden as compliant"
        else:
            result["reason"] = "Overridden as non-compliant"
        return result

    if att_type == "pull_request":
        pull_requests = attestation.get("pull_requests", [])
        if not pull_requests:
            result["reason"] = "No pull requests in attestation"
            return result

        for pr in pull_requests:
            approvers = pr.get("approvers", [])
            commits = pr.get("commits", [])

            if not approvers:
                result["reason"] = "Pull request has no approvers"
                return result

            # Clean up usernames (e.g., whitespace)
            approver_usernames = list(
                {a["username"].strip() for a in approvers if "username" in a}
            )
            if len(approver_usernames) >= 2:
                continue  # Passes this PR

            # Otherwise, check that ALL approvers are NOT in the commit authors
            commit_authors = [c.get("author_username") for c in commits]
            valid = approver_usernames[0].strip() not in commit_authors

            if not valid:
                result["reason"] = "The only approver of the PR is also a committer"
                return result

        result["pass"] = True
        result["reason"] = "Pull request demonstrates never-alone code review"
        return result

    result["reason"] = (
        f"Attestation is {att_type}, not a pull request or pull-request override"
    )
    return result


def evaluate_all(data):
    results = []
    for commit_hash, attestations in data.items():
        if not attestations:
            results.append(
                {
                    "commit": commit_hash,
                    "pass": False,
                    "reason": "No attestations found",
                    "attestation_url": None,
                }
            )
            continue

        # Evaluate only the first attestation
        result = evaluate_attestation(commit_hash, attestations[0])
        results.append(result)

    return results


def main():
    parser = argparse.ArgumentParser(description="Evaluate code review attestations")
    parser.add_argument("--host", default="http://localhost", help="API host URL")
    parser.add_argument("--org", required=True, help="Organization name")
    parser.add_argument("--flow", help="Flow name (optional)")
    parser.add_argument(
        "--commit-list", required=True, nargs="+", help="List of commit SHAs"
    )
    parser.add_argument(
        "--attestation-type",
        default="pull_request",
        help="Attestation type to filter by",
    )
    parser.add_argument(
        "--api-token", required=True, help="Kosli API token for authorization"
    )
    parser.add_argument("--input-file", help="Input JSON file (optional, for testing)")
    parser.add_argument(
        "--output-file",
        default="evaluation_results.json",
        help="Output JSON file (default: evaluation_results.json)",
    )

    args = parser.parse_args()

    if args.input_file:
        # Load from file for testing
        with open(args.input_file, "r") as f:
            data = json.load(f)
    else:
        # Make API request
        data = make_attestations_request(
            args.host,
            args.org,
            args.flow,
            args.commit_list,
            args.attestation_type,
            args.api_token,
        )

    output = evaluate_all(data)

    # Save output to file
    with open(args.output_file, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Evaluation results saved to: {args.output_file}")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
