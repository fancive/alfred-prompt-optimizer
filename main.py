import anthropic
import re
from subprocess import run
import os
import sys
from workflow import Workflow3
import json

# Assume the API key is set in the environment variables
api_key = os.environ.get("ANTHROPIC_API_KEY")
# Initialize Anthropic client
client = anthropic.Anthropic(api_key=api_key)
wf = Workflow3()

# Check if API key exists
if not api_key:
    wf.logger.error("ANTHROPIC_API_KEY not set")

    print(
        json.dumps(
            {
                "items": [
                    {
                        "title": "Error",
                        "subtitle": "ANTHROPIC_API_KEY not set",
                        "valid": False,
                    }
                ]
            }
        )
    )
    sys.exit(1)


def get_clipboard():
    from subprocess import check_output

    return check_output("pbpaste", env={"LANG": "en_US.UTF-8"}).decode("utf-8")


def set_clipboard(text):
    run("pbcopy", universal_newlines=True, input=text)


def extract_between_tags(tag: str, string: str, strip: bool = False) -> list[str]:
    ext_list = re.findall(f"<{tag}>(.+?)</{tag}>", string, re.DOTALL)
    if strip:
        ext_list = [e.strip() for e in ext_list]
    return ext_list


def remove_empty_tags(text):
    return re.sub(r"<(\w+)></\1>$", "", text)


def strip_last_sentence(text):
    sentences = text.split(". ")
    if sentences[-1].startswith("Let me know"):
        sentences = sentences[:-1]
        result = ". ".join(sentences)
        if result and not result.endswith("."):
            result += "."
        return result
    else:
        return text


def extract_prompt(metaprompt_response):
    between_tags = extract_between_tags("Instructions", metaprompt_response)[0]
    return remove_empty_tags(remove_empty_tags(between_tags).strip()).strip()


def extract_variables(prompt):
    pattern = r"{([^}]+)}"
    variables = re.findall(pattern, prompt)
    return set(variables)


def background_optimize(task):
    wf = Workflow3()
    wf.logger.debug(f"Starting background task optimization: {task[:50]}...")

    try:
        metaprompt = open("metaprompt.txt").read()
        prompt = metaprompt.replace("{{TASK}}", task)

        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )

        message = response.content[0].text
        extracted_prompt_template = extract_prompt(message)
        variables = extract_variables(extracted_prompt_template)

        set_clipboard(extracted_prompt_template)
        wf.logger.debug("Optimized prompt copied to clipboard")

        # Notify user that optimization is complete
        run(
            [
                "osascript",
                "-e",
                'display notification "Optimized prompt copied to clipboard" with title "Prompt Optimizer"',
            ]
        )

    except Exception as e:
        wf.logger.error(f"Error in background optimization: {str(e)}")
        run(
            [
                "osascript",
                "-e",
                f'display notification "Error: {str(e)}" with title "Prompt Optimizer"',
            ]
        )


def optimize_prompt(task):
    wf = Workflow3()
    wf.logger.debug(f"Starting task optimization: {task[:50]}...")

    try:
        metaprompt = open("metaprompt.txt").read()
        prompt = metaprompt.replace("{{TASK}}", task)

        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )

        message = response.content[0].text
        extracted_prompt_template = extract_prompt(message)
        variables = extract_variables(extracted_prompt_template)

        set_clipboard(extracted_prompt_template)
        wf.logger.debug("Optimized prompt copied to clipboard")

        return extracted_prompt_template, variables

    except Exception as e:
        wf.logger.error(f"Error in optimization: {str(e)}")
        return f"Error: {str(e)}", []


def main():
    wf = Workflow3()
    wf.logger.debug(f"Script started, arguments: {wf.args}")

    if len(wf.args) > 1 and wf.args[0] == "optimize":
        task = " ".join(wf.args[1:])
        wf.logger.debug(f"Executing optimization, task: {task[:50]}...")

        optimized_prompt, variables = optimize_prompt(task)

        if optimized_prompt.startswith("Error:"):
            print(
                json.dumps(
                    {
                        "alfredworkflow": {
                            "arg": "",
                            "variables": {"error": optimized_prompt},
                        }
                    }
                )
            )
        else:
            print(
                json.dumps(
                    {
                        "alfredworkflow": {
                            "arg": optimized_prompt,
                            "variables": {"variables": ", ".join(variables)},
                        }
                    }
                )
            )
    else:
        task = " ".join(wf.args) if wf.args else get_clipboard()
        wf.logger.debug(f"Preparing optimization, task: {task[:50]}...")
        print(
            json.dumps(
                {
                    "items": [
                        {
                            "title": "Optimize the following Prompt?",
                            "subtitle": task[:50] + "...",
                            "arg": task,
                            "valid": True,
                        }
                    ]
                }
            )
        )

    wf.logger.debug("Script execution completed")


if __name__ == "__main__":
    main()
