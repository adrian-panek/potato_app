package FlaskAppBuild.buildTypes

import jetbrains.buildServer.configs.kotlin.v2018_2.*
import jetbrains.buildServer.configs.kotlin.v2018_2.buildSteps.ScriptBuildStep
import jetbrains.buildServer.configs.kotlin.v2018_2.buildSteps.dockerCommand
import jetbrains.buildServer.configs.kotlin.v2018_2.buildSteps.script

object TestProject_Build : BuildType({
    id = AbsoluteId("TestProject_Build")
    name = "FullBuild"

    vcs {
        root(TestProject_FlaskApp)
    }

    steps {
        script {
            name = "List all downloaded files"
            scriptContent = "ls -a"
            dockerImage = "python"
            dockerImagePlatform = ScriptBuildStep.ImagePlatform.Linux
        }
        script {
            name = "Update dependency manager"
            scriptContent = "pip install --upgrade pip"
            dockerImagePlatform = ScriptBuildStep.ImagePlatform.Linux
        }
        script {
            name = "Cleanup previous pip installation"
            scriptContent = "cat requirements.txt | sudo xargs pip uninstall -y"
        }
        script {
            name = "Cleanup previous Docker image build"
            scriptContent = "docker rmi adrianpanek/python-app:latest"
        }
        script {
            name = "Install all required dependencies"
            scriptContent = "pip install -r requirements.txt"
            dockerImagePlatform = ScriptBuildStep.ImagePlatform.Linux
        }
        script {
            name = "Run static code analysis"
            scriptContent = """find -name "*.py" -not -path "./venv/*" | xargs pylint -E --load-plugins=pylint_flask | tee pylint.log"""
            dockerImagePlatform = ScriptBuildStep.ImagePlatform.Linux
        }
        script {
            name = "Run tests"
            scriptContent = "python3 -m pytest"
            dockerImagePlatform = ScriptBuildStep.ImagePlatform.Linux
        }
        dockerCommand {
            name = "Build image"
            executionMode = BuildStep.ExecutionMode.RUN_ON_FAILURE
            commandType = build {
                source = file {
                    path = "Dockerfile"
                }
            }
        }
    }
})