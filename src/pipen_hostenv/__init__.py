from __future__ import annotations

import os
from typing import TYPE_CHECKING
from dotenv import dotenv_values
from pipen import plugin

if TYPE_CHECKING:
    from pipen import Pipen
    from pipen.job import Job

__version__ = "0.0.1"


class PipenHostEnv:
    __version__ = __version__
    name = "hostenv"

    @plugin.impl
    def on_setup(pipen: Pipen) -> None:  # pyright: ignore[reportGeneralTypeIssues]
        """Default configurations"""
        # pipeline level: name or detailed theme
        pipen.config.plugin_opts.hostenv_file = "./.env"
        pipen.config.plugin_opts.hostenv_values = {}

    @plugin.impl
    async def on_job_init(job: Job) -> None:  # pyright: ignore[reportGeneralTypeIssues]
        """Load host environment variables"""


        env_file = (
            job
            .proc
            .plugin_opts  # pyright: ignore[reportOptionalMemberAccess]
            .get(  # pyright: ignore[reportOptionalMemberAccess]
                "hostenv_file",
                "./.env",
            )
        )
        env_values = (
            job
            .proc
            .plugin_opts  # pyright: ignore[reportOptionalMemberAccess]
            .get("hostenv_values", {})  # pyright: ignore[reportOptionalMemberAccess]
        )
        if env_file and os.path.exists(env_file):
            envs = dotenv_values(env_file)
            job.envs.update(envs)
        job.envs.update(env_values)
