import click
import traceback

from lib.tg_bot import send_tg_message


class SendReportCommand:
    def __init__(self, txt_file_path: str, is_sync_success: bool):
        self.txt_file_path: str = txt_file_path
        self.is_sync_success: bool = is_sync_success

    def execute(self):
        try:
            with open(self.txt_file_path, 'r') as f:
                prefix_text = 'OK' if self.is_sync_success else 'ERROR'
                file_contents = f.read()
                message = f"[{prefix_text}]\n{file_contents}"
                send_tg_message(message)
                click.echo(click.style('Success', fg="green"))

        except Exception as e:
            click.echo(click.style(str(e), fg="red"))
            click.echo(click.style("Error on send report", fg='red'))
            print(traceback.format_exc())
            raise e
