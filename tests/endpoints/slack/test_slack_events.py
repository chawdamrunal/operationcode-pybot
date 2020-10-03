import asyncio
import logging

import asynctest
from asynctest import CoroutineMock

from pybot import endpoints
from pybot.endpoints.slack.events import create_endpoints, team_join
from tests.data.events import MESSAGE_DELETE, MESSAGE_EDIT, PLAIN_MESSAGE, TEAM_JOIN


async def test_team_join_handler_exists(bot):
    endpoints.slack.create_endpoints(bot["plugins"]["slack"])

    assert asynctest.asyncio.iscoroutinefunction(
        bot["plugins"]["slack"].routers["event"]._routes["team_join"]["*"]["*"][0][0] 
    )


async def test_edits_are_logged(bot, aiohttp_client, caplog):
    client = await aiohttp_client(bot)

    with caplog.at_level(logging.INFO):
        await client.post("/slack/events", json=MESSAGE_EDIT)
    assert any("CHANGE_LOGGING: edited" in record.message for record in caplog.records)


async def test_deletes_are_logged(bot, aiohttp_client, caplog):
    client = await aiohttp_client(bot)

    with caplog.at_level(logging.INFO):
        await client.post("/slack/events", json=MESSAGE_DELETE)
    assert any("CHANGE_LOGGING: deleted" in record.message for record in caplog.records)


async def test_no_other_messages_logged(bot, aiohttp_client, caplog):
    client = await aiohttp_client(bot)

    with caplog.at_level(logging.INFO):
        await client.post("/slack/events", json=PLAIN_MESSAGE)
    assert not any("CHANGE_LOGGING" in record.message for record in caplog.records)
