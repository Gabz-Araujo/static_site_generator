from typing import List, Dict, Optional, Union

PropsDict = Dict[str, str]


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[List["HTMLNode"]] = None,
        props: Optional[PropsDict] = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError("Not Implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        propsStr = " ".join(f'{key}="{value}"' for key, value in self.props.items())
        return f"{propsStr}"

    def __repr__(self):
        return (
            f"HTMLNode(tag={self.tag!r}, "
            f"value={self.value!r}, "
            f"children={self.children!r}, "
            f"props={self.props!r})"
        )


class LeafNode(HTMLNode):
    def __init__(
        self,
        value: str,
        tag: Optional[str] = None,
        children: Optional[List[HTMLNode]] = None,
        props: Optional[PropsDict] = None,
    ):
        super().__init__(tag, value, children, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Value can't be None")
        if self.tag is None:
            return f"{self.value}"
        if self.props:
            props = self.props_to_html()
            return f"<{self.tag} {props}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"

    def __repr__(self):
        return (
            f"LeafNode(tag={self.tag!r}, "
            f"value={self.value!r}, "
            f"children={self.children!r}, "
            f"props={self.props!r})"
        )


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: List[Union[HTMLNode, LeafNode, "ParentNode"]],
        props: Optional[PropsDict] = None,
    ):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag can't be None")
        if self.children is None:
            raise ValueError("Children can't be None")
        props = self.props_to_html()
        children_html = "".join(child.to_html() for child in self.children)
        if props:
            return f"<{self.tag} {props}>{children_html}</{self.tag}>"
        return f"<{self.tag}>{children_html}</{self.tag}>"

    def __repr__(self):
        return (
            f"ParentNode(tag={self.tag!r}, "
            f"children={self.children!r}, "
            f"props={self.props!r})"
        )
