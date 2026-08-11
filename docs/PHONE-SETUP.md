# Using Claude Code from Your Phone

Claude Code doesn't run *on* the phone — every session runs in a cloud
container that clones your repo, does the work, and pushes the result back to
GitHub as a branch/pull request. Your phone is just the remote control, so
nothing needs to be installed beyond the Claude app.

## One-time setup

1. Install the **Claude app** (iOS App Store / Google Play) and sign in with
   the same account you use on claude.ai — or just open
   [claude.ai/code](https://claude.ai/code) in your phone's browser.
2. Open the **Code** section of the app (or claude.ai/code).
3. If GitHub isn't connected yet, follow the prompt to install the **Claude
   GitHub App** and grant it access to the repositories you want to work on.
   You can change which repos it can see anytime at
   [github.com/settings/installations](https://github.com/settings/installations).

## Daily use

1. Open Code in the Claude app.
2. Pick a repository (e.g. this one) and type what you want done.
3. Claude works in the cloud — you can lock your phone, switch apps, or come
   back later; the session keeps running.
4. Results arrive as a branch and a draft pull request. Review and merge from
   the **GitHub mobile app** (recommended install) or github.com.

## Creating a new repository

The Claude GitHub integration can read and push to repos you've granted it,
but it is **not allowed to create repositories** on your account — that part
takes about a minute by hand:

1. Go to [github.com/new](https://github.com/new) (works fine in a phone
   browser, or use the GitHub mobile app: **Profile → Repositories → +**).
2. Name it, choose **Private**, tick **Add a README file** (so it isn't
   empty), and create it.
3. Grant the Claude GitHub App access to it at
   [github.com/settings/installations](https://github.com/settings/installations)
   → Claude → Repository access → **Select repositories** → add the new repo.
4. It now shows up in the repo picker at claude.ai/code — start a session and
   go.

## Tips

- One repo can hold many unrelated projects (this repo already mixes smoker
  hardware and other work), but separate repos keep history and PRs cleaner.
- Claude pushes to `claude/...` branches and opens draft PRs — nothing lands
  on your default branch until you merge it.
- You can ask Claude to keep watching a PR ("babysit this PR") and it will
  react to CI failures and review comments on its own.
