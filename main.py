from __future__ import annotations

from typing import Dict, Any

from fastapi import FastAPI, Depends
from fastapi.routing import APIRoute
from fastapi.dependencies.models import Dependant
from rich.console import Console

from tree import Node

app = FastAPI()


def another() -> None:
    ...


def something(dep: None = Depends(another)) -> None:
    ...


@app.get("/")
def home(a: None = Depends(something), b: None = Depends(another)):
    ...


console = Console()


def build_dependency_tree(dependant: Dependant, tree: Node | None = None) -> Node:
    name = getattr(dependant.call, "__name__", None)
    tree = tree or Node(name=name, children=[])
    for dependant in dependant.dependencies:
        name = getattr(dependant.call, "__name__", None)
        sub_tree = Node(name=name, children=[])
        build_dependency_tree(dependant=dependant, tree=sub_tree)
        tree.children.append(sub_tree)
    return tree


def find_dependencies(app: FastAPI) -> Dict[str, Any]:
    endpoints = {}
    for route in app.routes:
        if not isinstance(route, APIRoute):
            continue
        deps_tree = [build_dependency_tree(dep) for dep in route.dependant.dependencies]
        endpoints[route.unique_id] = {"name": route.name, "dependencies": deps_tree}

    return endpoints


if __name__ == "__main__":
    console.print(find_dependencies(app=app))

# TODO: Use graphz to generate the Graph. Each rectangle should be an endpoint, and
# inside we should have circles as dependencies (nodes).
