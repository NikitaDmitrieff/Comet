import asyncio
import os

import pytest
from comet_helper.main import GuidanceCounselor


@pytest.mark.asyncio
async def test_ask():

    guidance_counselor = GuidanceCounselor(
        pdf_directory=os.getenv("COMET_HELPER_DATA_PATH"),
    )

    output = await guidance_counselor.generate_answer(user_question="say hi")

    assert output


asyncio.run(test_ask())
