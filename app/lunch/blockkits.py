from app.core.blockkit import (
    Block,
    CardBlockkit,
    Context,
    Divider,
    Header,
    Section,
    Text,
)
from app.core.timezone import SEOUL

from .models import Attendance, Lunch, Roulette


def left_context(roulette: Roulette):
    return Context(
        elements=[
            Text(
                text=f":hourglass_flowing_sand: *{roulette.countdown // 60} minutes left* "
                f"| {roulette.spin_at.astimezone(tz=SEOUL).strftime('%c')}"
            )
        ]
    )


def howto_context(roulette: Roulette):
    return Context(elements=[Text(text=":pushpin: Here is *how to join lunch roulette*.")])


class RouletteOpenBlockKit(CardBlockkit):
    def __init__(self, roulette: Roulette):
        self.roulette = roulette

    def header(self) -> list[Block]:
        return [
            Header(
                text=Text(
                    type=Text.Type.plain_text,
                    text=":knife_fork_plate: Lunch Roulette is Open! :confetti_ball:",
                )
            ),
            left_context(roulette=self.roulette),
            Divider(),
        ]

    def body(self) -> list[Block]:
        return [
            Section(text=Text(text=":loud_sound: *Join right now!* :yum::fork_and_knife:")),
            Section(text=Text(text="`/godabot-lunch your preference as a free from`")),
            Section(
                text=Text(
                    text="Here is slashcommand examples\n "
                    "- `godabot-lunch I'd like to go a pizza restaurant`\n "
                    "- `godabot-lunch I love Japanese food`\n "
                    "- `godabot-lunch Anything, whatever you like`"
                )
            ),
            Section(text=Text(text="This line is a lorem ipsum.")),
            Divider(),
        ]

    def footer(self) -> list[Block]:
        return [howto_context(roulette=self.roulette)]


class RouletteSpunBlockKit(CardBlockkit):
    def __init__(self, roulette: Roulette):
        self.roulette = roulette

    def header(self) -> list[Block]:
        return [
            Header(
                text=Text(
                    type=Text.Type.plain_text,
                    text=":knife_fork_plate: Have a good lunch! :confetti_ball:",
                )
            ),
            Context(
                elements=[
                    Text(
                        text=f":yum: *{len(self.roulette.lunches)} lunches with "
                        f"{len(self.roulette.attendances)} attendees* "
                        f"| {self.roulette.spin_at.strftime('%c')}"
                    )
                ]
            ),
            Divider(),
        ]

    def body(self) -> list[Block]:
        def lunch_block(no: int, lunch: Lunch):
            return [
                Section(text=Text(text=f"*{no}. {lunch.title} | {lunch.preference}*")),
                Context(
                    elements=[
                        Text(text=", ".join(attendance.mention for attendance in lunch.attendances))
                    ]
                ),
                Section(text=Text(text=f">:receipt: {lunch.recommendation}")),
            ]

        lunch_blocks = (
            lunch_block(no=no, lunch=lunch)
            for no, lunch in enumerate(self.roulette.lunches, start=1)
        )

        return [
            Section(text=Text(text=":loud_sound: *Here is the result.* :yum::fork_and_knife:")),
            *sum(lunch_blocks, start=[]),
            Divider(),
            Section(text=Text(text=":busts_in_silhouette: *Attendee List*")),
            Context(
                elements=[
                    Text(
                        text="\n".join(
                            f"- {attendance.user_name} | {attendance.preference}\n"
                            for attendance in self.roulette.attendances
                        )
                    )
                ]
            ),
            Divider(),
        ]

    def footer(self) -> list[Block]:
        return [howto_context(roulette=self.roulette)]


class AttendanceJoinedBlockKit(CardBlockkit):
    def __init__(self, *, attendance: Attendance):
        self.attendance = attendance

    def header(self):
        return [
            Header(
                text=Text(
                    type=Text.Type.plain_text,
                    text=f":knife_fork_plate: {self.attendance.user_name} is joined:confetti_ball:",
                ),
            ),
            left_context(roulette=self.attendance.roulette),
            Divider(),
        ]

    def body(self):
        return [
            Section(
                text=Text(
                    text=f":busts_in_silhouette: "
                    f"*{len(self.attendance.roulette.attendances)} attendees* are joined... "
                    f":yum::fork_and_knife:"
                )
            ),
            Section(
                text=Text(
                    text=", ".join(
                        f"`{attendance.user_name}`"
                        for attendance in self.attendance.roulette.attendances
                    )
                )
            ),
            Section(text=Text(text="This line is a lorem ipsum.")),
            Divider(),
        ]

    def footer(self) -> list[Block]:
        return [howto_context(roulette=self.attendance.roulette)]
