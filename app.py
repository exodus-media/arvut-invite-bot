from aiogram.types import BotCommand

from data.config import DEBUG
from loader import _, bot
from utils.db_api import create_table


async def set_commands(bot):
    commands = [
        BotCommand(command="/start", description="Main menu")
    ]
    await bot.set_my_commands(commands)


async def on_startup(dp):
    import middlewares
    middlewares.setup(dp)

    await create_table.run()
    await set_commands(bot)


async def on_startup_web_hook(app):
    # Get current webhook status
    webhook = await bot.get_webhook_info()
    await create_table.run()
    await set_commands(bot)

    # If URL is bad
    if webhook.url != WEBHOOK_URL:
        # If URL doesnt match current - remove webhook
        if not webhook.url:
            await bot.delete_webhook()

        # Set new URL for webhook
        await bot.set_webhook(WEBHOOK_URL, certificate=open(WEBHOOK_SSL_CERT, 'rb'))
        # If you want to use free certificate signed by LetsEncrypt you need to set only URL without sending
        # certificate.


async def on_shutdown_web_hook(app):
    """
    Graceful shutdown. This method is recommended by aiohttp docs.
    """
    # Remove webhook.
    await bot.delete_webhook()

    # Close Redis connection.
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == '__main__':
    from handlers import dp
    if DEBUG:
        from aiogram import executor
        executor.start_polling(dp, on_startup=on_startup)
    else:
        import ssl
        from aiohttp import web
        from aiogram.dispatcher.webhook import get_new_configured_app
        from data.config import WEBHOOK_URL, WEBHOOK_SSL_CERT, WEBHOOK_URL_PATH, WEBHOOK_SSL_PRIV, \
            WEBHOOK_LISTEN, WEBHOOK_PORT

        # Get instance of :class:`aiohttp.web.Application` with configured router.
        app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_URL_PATH)

        # Setup event handlers.
        app.on_startup.append(on_startup_web_hook)
        app.on_shutdown.append(on_shutdown_web_hook)

        # Generate SSL context
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

        # Start web-application.
        web.run_app(app, host=WEBHOOK_LISTEN, port=WEBHOOK_PORT, ssl_context=context)
