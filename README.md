# Prompt Optimizer Alfred Workflow

## Introduction

Prompt Optimizer is an Alfred Workflow designed to enhance and refine prompts for AI interactions. It leverages Anthropic's Claude AI to analyze and improve prompts, making them more effective and precise for various AI applications.

## Features

- Optimize prompts from clipboard or direct input
- Utilize Anthropic's Claude AI for intelligent optimization
- Automatically copy optimized prompts to clipboard
- Identify variables within prompts
- Seamless integration with Alfred for a smooth user experience

## Installation

1. Ensure you have [Alfred](https://www.alfredapp.com/) installed with the Powerpack license.
2. Download the latest `PromptOptimizer.alfredworkflow` file from the releases page.
3. Double-click the downloaded file to install the Workflow in Alfred.

## Configuration

1. Open Alfred Preferences and navigate to the Workflows tab.
2. Find the Prompt Optimizer workflow.
3. Right-click on the workflow and select "Show in Finder" to open the workflow directory.
4. Create a file named `metaprompt.txt` in this directory and paste your metaprompt content.
5. In the workflow configuration, add your Anthropic API key to the `ANTHROPIC_API_KEY` environment variable:
   - Click the [x] button in the top-right corner of the workflow.
   - Add a new environment variable named `ANTHROPIC_API_KEY`.
   - Paste your Anthropic API key as the value.

## Usage

1. In Alfred, type the keyword `po` followed by the prompt you want to optimize.
   Example: `po Generate an outline for an article about climate change`

2. Alternatively, copy the prompt you want to optimize to your clipboard, then type `po` in Alfred.

3. Press Enter to confirm and start the optimization process.

4. Wait for the optimization to complete. You'll see a notification when it's done.

5. The optimized prompt will be automatically copied to your clipboard.

## Dependencies

- Python 3.7+
- anthropic
- alfred-workflow

These dependencies are included in the workflow package. No additional installation is required.

## Troubleshooting

If you encounter any issues:

1. Ensure you've correctly set up the `ANTHROPIC_API_KEY` in the workflow environment variables.
2. Check the log information in Alfred's debug console:
   - Open Alfred Preferences > Workflows
   - Select the Prompt Optimizer workflow
   - Click the [x] button in the top-right corner
   - Click "Open workflow logs in Console"
3. Make sure the `metaprompt.txt` file exists in the Workflow directory and contains the correct content.

## Contributing

Issues and pull requests are welcome to help improve this project. Please feel free to contribute to the code, documentation, or by reporting bugs.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions, suggestions, or need assistance, please open an issue on the GitHub repository or contact the maintainer at [your contact information].

## Acknowledgements

- This project uses the Anthropic API to leverage Claude AI for prompt optimization.
- Thanks to the Alfred team for creating such a powerful productivity tool.