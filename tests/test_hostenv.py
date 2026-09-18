import pytest
import os
from pathlib import Path
from pipen import Proc, run


def test_hostenv_loads_cwd_dotenv():

    class P1(Proc):
        cache = False
        input = "name:var"
        output = "o:file:{{in.name}}.txt"
        script = "echo ${{in.name}} > {{out.o}}"

    run("HostEnvLoadsCwdEnvfile", starts=P1, data=["VAR"])
    outfile = "HostEnvLoadsCwdEnvfile-output/P1/VAR.txt"

    assert Path(outfile).exists()
    assert Path(outfile).read_text().strip() == "hello world"


def test_hostenv_loads_custom_dotenv():

    class P2(Proc):
        cache = False
        input = "name:var"
        output = "o:file:{{in.name}}.txt"
        script = "echo ${{in.name}} > {{out.o}}"
        plugin_opts = {"hostenv_file": "./envfile"}

    run(
        "HostEnvLoadsCustomEnvfile",
        starts=P2,
        data=["VAR2"],
    )
    outfile = "HostEnvLoadsCustomEnvfile-output/P2/VAR2.txt"

    assert Path(outfile).exists()
    assert Path(outfile).read_text().strip() == "blue sky"


def test_hostenv_loads_from_pipeline_config():

    class P3(Proc):
        cache = False
        input = "name:var"
        output = "o:file:{{in.name}}.txt"
        script = "echo ${{in.name}} > {{out.o}}"

    run(
        "HostEnvLoadsPipelineConfig",
        starts=P3,
        data=["VAR2"],
        plugin_opts={"hostenv_file": "./envfile"},
    )
    outfile = "HostEnvLoadsPipelineConfig-output/P3/VAR2.txt"

    assert Path(outfile).exists()
    assert Path(outfile).read_text().strip() == "blue sky"


def test_hostenv_loads_direct_passed_envs():

    class P4(Proc):
        cache = False
        input = "name:var"
        output = "o:file:{{in.name}}.txt"
        script = "echo ${{in.name}} > {{out.o}}"

    run(
        "HostEnvLoadsDirectPassedEnvs",
        starts=P4,
        data=["VAR3"],
        plugin_opts={"hostenv_values": {"VAR3": "green grass"}},
    )
    outfile = "HostEnvLoadsDirectPassedEnvs-output/P4/VAR3.txt"

    assert Path(outfile).exists()
    assert Path(outfile).read_text().strip() == "green grass"


def test_hostenv_direct_envs_override_dotenv():

    class P5(Proc):
        cache = False
        input = "name:var"
        output = "o:file:{{in.name}}.txt"
        script = "echo ${{in.name}} > {{out.o}}"

    run(
        "HostEnvDirectEnvsOverrideDotenv",
        starts=P5,
        data=["VAR"],
        plugin_opts={
            "hostenv_file": "./.env",
            "hostenv_values": {"VAR": "override value"},
        },
    )
    outfile = "HostEnvDirectEnvsOverrideDotenv-output/P5/VAR.txt"

    assert Path(outfile).exists()
    assert Path(outfile).read_text().strip() == "override value"
