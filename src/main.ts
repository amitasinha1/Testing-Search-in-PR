const core = require('@actions/core');
const github = require('@actions/github')
const parse = require('parse-diff')

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

    // Get changed chunks
    var changes = ''
    var additions: number = 0
    files.forEach(function(file) {
      additions += file.additions
      file.chunks.forEach(function(chunk) {
        chunk.changes.forEach(function(change) {
          if (change.add) {
            changes += change.content
          }
        })
      })
    })

    // Check that the pull request diff does not contain the forbidden string
    const diffDoesNotContain = core.getInput('diffDoesNotContain')
    if (diffDoesNotContain && changes.includes(diffDoesNotContain)) {
      core.setFailed("The PR diff should not include " + diffDoesNotContain);
    }

  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
