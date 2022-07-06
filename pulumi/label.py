import pulumi
from dynamic_providers.github.label import GithubLabel, GithubLabelArgs

label = GithubLabel("foo", GithubLabelArgs("lukehoban", "todo", "mylabel", "d94f0b"))

pulumi.export("label_color", label.color)
pulumi.export("label_url", label.url)