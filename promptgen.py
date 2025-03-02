# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "anthropic==0.49.0",
#     "instructor==1.7.2",
#     "marimo",
#     "mohtml==0.1.2",
#     "pydantic==2.10.6",
#     "python-dotenv==1.0.1",
# ]
# ///

import marimo

__generated_with = "0.11.2"
app = marimo.App(width="medium")


@app.cell
def _():
    from mohtml import p
    import marimo as mo
    return mo, p


@app.cell
def _():
    from typing import List
    import instructor
    from pydantic import BaseModel


    class ImageDescription(BaseModel):
        """
        Take the input sentence and describe it visually for a Midjourney prompt such that we have a proper scene that could be useful in a movie trailer. Make sure that you keep the style in mind as well. Also add a small prompt for a text-to-video service like runway. Make sure to use descriptions of camera angles here. 
        """
        midjourney_desc: str
        runway_desc: str
    return BaseModel, ImageDescription, List, instructor


@app.cell
def _(instructor):
    from instructor import Instructor, Mode, patch
    from anthropic import Anthropic
    from dotenv import load_dotenv
    import os

    load_dotenv(".env")

    client = instructor.from_anthropic(
        Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"]),
    )
    return Anthropic, Instructor, Mode, client, load_dotenv, os, patch


@app.cell
def _(ImageDescription, client):
    def to_midjourney(scene, style):
        return client.chat.completions.create(
            model="claude-3-5-sonnet-20241022",
            messages=[
                {
                    "role": "user",
                    "content": f"{scene} in the style of {style}",
                }
            ],
            max_tokens=1500,
            response_model=ImageDescription,
        )

    out = to_midjourney("the citadel from mass effect", "70ies movie")
    return out, to_midjourney


@app.cell
def _(out, p):
    p(out.midjourney_desc)
    return


@app.cell
def _(out, p):
    p(out.runway_desc)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
