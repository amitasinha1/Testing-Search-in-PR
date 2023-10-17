import * as core from "@actions/core";
const { GitHub, context } = require("@actions/github");
import parse from "parse-diff";
import { rexify } from "./utils";

async function run() {
  try {
    // get information on everything
    const token = core.getInput('github-token', { required: true })
    const octokit = github.getOctokit(token)
    const context = github.context

    // Request the pull request diff from the GitHub API
    const { data: prDiff } = await octokit.pulls.get({
      owner: context.repo.owner,
      repo: context.repo.repo,
      pull_number: context.payload.pull_request.number,
      mediaType: {
        format: "diff",
      },
    });
    const files = parse(prDiff)

    // Check that the pull request diff does not contain the forbidden string
    const diffDoesNotContain = core.getInput('diffDoesNotContain')
    if (diffDoesNotContain && rexify(diffDoesNotContain).test(changes)) {
          core.setFailed(
            "The added code should not contain " + diffDoesNotContain
          );
    }

  } catch (error) {
    core.setFailed(error.message);
  }

}
run();
