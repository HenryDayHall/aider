def scrub_sensitive_info(args, text):
    # Replace sensitive information with last 4 characters
    if text and args.openai_api_key:
        last_4 = args.openai_api_key[-4:]
        text = text.replace(args.openai_api_key, f"...{last_4}")
    if text and args.anthropic_api_key:
        last_4 = args.anthropic_api_key[-4:]
        text = text.replace(args.anthropic_api_key, f"...{last_4}")
    return text


def format_settings_output(parser, args, coder):
    """Build the same text that the /settings command prints."""
    settings = format_settings(parser, args)
    announcements = "\n".join(coder.get_announcements())

    model_sections = []
    active_models = [
        ("Main model", coder.main_model),
        ("Editor model", getattr(coder.main_model, "editor_model", None)),
        ("Weak model", getattr(coder.main_model, "weak_model", None)),
    ]
    for label, model in active_models:
        if not model:
            continue
        info = getattr(model, "info", {}) or {}
        if not info:
            continue
        model_sections.append(f"{label} ({model.name}):")
        for k, v in sorted(info.items()):
            model_sections.append(f"  {k}: {v}")
        model_sections.append("")  # blank line between models

    model_metadata = "\n".join(model_sections)

    output = f"{announcements}\n{settings}"
    if model_metadata:
        output += "\n" + model_metadata
    return output


def format_settings(parser, args):
    show = scrub_sensitive_info(args, parser.format_values())
    # clean up the headings for consistency w/ new lines
    heading_env = "Environment Variables:"
    heading_defaults = "Defaults:"
    if heading_env in show:
        show = show.replace(heading_env, "\n" + heading_env)
        show = show.replace(heading_defaults, "\n" + heading_defaults)
    show += "\n"
    show += "Option settings:\n"
    for arg, val in sorted(vars(args).items()):
        if val:
            val = scrub_sensitive_info(args, str(val))
        show += f"  - {arg}: {val}\n"  # noqa: E221
    return show
