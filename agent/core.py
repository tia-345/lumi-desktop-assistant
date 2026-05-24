import json
import re
import subprocess

from llm.ollama_client import query_llm

from tools.file_tools import (
    read_file,
    write_file
)

from tools.platform import (
    open_file,
    search_web,
    search_youtube,
    send_whatsapp_message,
    send_whatsapp_group_message,
    open_app,
    close_app,
    list_files,
    run_command,
    get_time,
    get_date,
    compose_email,
    get_weather
)

from memory.knowledge import add_memory

from config import (
    MODEL,
    CONTENT_MODEL
)


# =========================================================
# CLOSE APP TRIGGERS
# =========================================================

CLOSE_TRIGGERS = [
    "close ",
    "quit ",
    "kill ",
    "exit ",
    "stop ",
    "shut down "
]


# =========================================================
# DETECT CLOSE REQUEST
# =========================================================

def is_close_request(user_input):

    text = user_input.lower().strip()

    for trigger in CLOSE_TRIGGERS:

        if text.startswith(trigger):

            return text.replace(
                trigger,
                "",
                1
            ).strip()

    return None


# =========================================================
# EXECUTE TOOL
# =========================================================

def execute_tool(tool, args):

    if tool == "get_time":

        return get_time()

    elif tool == "get_date":

        return get_date()

    elif tool == "get_weather":

        return get_weather(
            args.get("city", "Kochi")
        )

    elif tool == "open_file":

        return open_file(
            args.get("path")
        )

    elif tool == "open_anything":

        name = args.get("name")

        if name and "." in name:
            return open_file(name)

        return open_app(name)

    elif tool == "open_app":

        return open_app(
            args.get("name")
        )

    elif tool == "close_app":

        return close_app(
            args.get("name")
        )

    elif tool == "list_files":

        return list_files(
            args.get("path", ".")
        )

    elif tool == "run_command":

        return run_command(
            args.get("command")
        )

    elif tool == "search_web":

        return search_web(
            args.get("query")
        )

    elif tool == "search_youtube":

        return search_youtube(
            args.get("query")
        )

    elif tool == "send_whatsapp_message":

        return send_whatsapp_message(
            args.get("contact"),
            args.get("message")
        )

    elif tool == "send_whatsapp_group_message":

        return send_whatsapp_group_message(
            args.get("group_name"),
            args.get("message")
        )

    elif tool == "compose_email":

        return compose_email(
            args.get("receiver"),
            args.get("subject"),
            args.get("body")
        )

    return "Unknown tool"


# =========================================================
# SIMPLE INTENT PARSER
# =========================================================

def simple_intent_parser(user_input):

    text = user_input.lower().strip()

    # -----------------------------------------------------
    # TIME
    # -----------------------------------------------------

    if "time" in text:

        return {
            "type": "action",
            "tool": "get_time",
            "args": {}
        }

    # -----------------------------------------------------
    # DATE
    # -----------------------------------------------------

    if "date" in text or "today" in text:

        return {
            "type": "action",
            "tool": "get_date",
            "args": {}
        }

    # -----------------------------------------------------
    # WEATHER
    # -----------------------------------------------------

    if "weather" in text:

        city = "Kochi"

        if "in " in text:
            city = text.split("in ")[-1].strip()

        return {
            "type": "action",
            "tool": "get_weather",
            "args": {
                "city": city
            }
        }

    # -----------------------------------------------------
    # EMAIL
    # -----------------------------------------------------

    if "send email to" in text:

        try:

            receiver = (
                text.split("to")[1]
                .split("subject")[0]
                .strip()
            )

            subject = (
                text.split("subject")[1]
                .split("body")[0]
                .strip()
            )

            body = (
                text.split("body")[1]
                .strip()
            )

            return {
                "type": "action",
                "tool": "compose_email",
                "args": {
                    "receiver": receiver,
                    "subject": subject,
                    "body": body
                }
            }

        except:

            return {
                "type": "answer",
                "content": (
                    "Use format:\n"
                    "send email to abc@gmail.com "
                    "subject Hello "
                    "body How are you"
                )
            }

    # -----------------------------------------------------
    # OPEN WHATSAPP
    # -----------------------------------------------------

    if (
        "open whatsapp" in text
        or text == "whatsapp"
    ):

        return {
            "type": "action",
            "tool": "open_anything",
            "args": {
                "name": "WhatsApp"
            }
        }

    # -----------------------------------------------------
    # SEND WHATSAPP GROUP MESSAGE
    # -----------------------------------------------------

    if "send whatsapp group message" in text:

        try:

            group_name = (
                text.split("to")[1]
                .split("saying")[0]
                .strip()
            )

            message = (
                text.split("saying")[1]
                .strip()
            )

            return {
                "type": "action",
                "tool": "send_whatsapp_group_message",
                "args": {
                    "group_name": group_name,
                    "message": message
                }
            }

        except:

            return {
                "type": "answer",
                "content": (
                    "Use format:\n"
                    "send whatsapp group message "
                    "to Group Name saying hello"
                )
            }

    # -----------------------------------------------------
    # SEND WHATSAPP MESSAGE
    # -----------------------------------------------------

    if "send whatsapp message" in text:

        try:

            contact = (
                text.split("to")[1]
                .split("saying")[0]
                .strip()
            )

            message = (
                text.split("saying")[1]
                .strip()
            )

            return {
                "type": "action",
                "tool": "send_whatsapp_message",
                "args": {
                    "contact": contact,
                    "message": message
                }
            }

        except:

            return {
                "type": "answer",
                "content": (
                    "Use format:\n"
                    "send whatsapp message "
                    "to 9447571550 saying hello"
                )
            }

    # -----------------------------------------------------
    # SEARCH YOUTUBE
    # -----------------------------------------------------

    if "youtube" in text:

        query = text

        query = query.replace(
            "search youtube for",
            ""
        )

        query = query.replace(
            "search youtube",
            ""
        )

        query = query.replace(
            "youtube",
            ""
        )

        query = query.strip()

        return {
            "type": "action",
            "tool": "search_youtube",
            "args": {
                "query": query
            }
        }

    # -----------------------------------------------------
    # SEARCH WEB
    # -----------------------------------------------------

    if (
        "search" in text
        and "whatsapp" not in text
    ):

        query = text

        query = query.replace(
            "open chrome and search",
            ""
        )

        query = query.replace(
            "search google for",
            ""
        )

        query = query.replace(
            "search for",
            ""
        )

        query = query.replace(
            "search",
            ""
        )

        query = query.strip()

        return {
            "type": "action",
            "tool": "search_web",
            "args": {
                "query": query
            }
        }

    # -----------------------------------------------------
    # OPEN APP
    # -----------------------------------------------------

    if text.startswith("open "):

        name = text.replace(
            "open",
            "",
            1
        ).strip()

        return {
            "type": "action",
            "tool": "open_anything",
            "args": {
                "name": name
            }
        }

    # -----------------------------------------------------
    # CLOSE APP
    # -----------------------------------------------------

    app_name = is_close_request(
        user_input
    )

    if app_name:

        return {
            "type": "action",
            "tool": "close_app",
            "args": {
                "name": app_name
            }
        }

    return None


# =========================================================
# CLEAN RESPONSE
# =========================================================

def extract_clean_response(data):

    if isinstance(data, dict):

        if data.get("type") == "answer":
            return data.get("content", "")

        if data.get("type") == "action":
            return data

    if isinstance(data, str):

        data = re.sub(
            r'\x1b\[[0-9;]*[a-zA-Z]',
            '',
            data
        )

        data = re.sub(
            r'<[^>]+>',
            '',
            data
        )

        data = re.sub(
            r'```json|```',
            '',
            data
        )

        data = data.strip()

        if not data:
            return "I couldn't generate a valid response."

        return data

    return "I'm sorry, I couldn't process that request."


# =========================================================
# MAIN AGENT LOOP
# =========================================================

def run_agent(user_input):

    # Local parser first
    local_intent = simple_intent_parser(
        user_input
    )

    if local_intent:

        processed = local_intent

    else:

        # Ask LLM
        raw_response = query_llm(
            user_input
        )

        processed = extract_clean_response(
            raw_response
        )

    # Plain response
    if isinstance(processed, str):
        return processed

    # Tool execution
    if isinstance(processed, dict):

        if processed.get("type") == "action":

            tool = processed.get("tool")

            args = processed.get("args", {})

            result = execute_tool(
                tool,
                args
            )

            add_memory({
                "input": user_input,
                "tool": tool,
                "args": args,
                "result": result
            })

            return f"[RESULT]: {result}"

        if processed.get("type") == "answer":

            return processed.get(
                "content",
                ""
            ).strip()

    return "I'm sorry, I couldn't process that request."

