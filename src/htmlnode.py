# define HTML Node class
class HTMLNode:
    def __init__(self,  tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children if children is not None else [] 
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        result = " ".join([f'{key}="{value}" ' for key, value in self.props.items()])
        return result

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

# Define LeafNode class
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None) -> None:
        super().__init__(tag=tag, value=value,children=None,props=props)
        if self.value == None:
            raise ValueError("LeafNode must have a value!")


    def to_html(self):
        if self.tag in ["img", "br", "hr"]:
            if self.props:
                return f"<{self.tag} {self.props_to_html()} />"
            else:
                return f"<{self.tag} />"
        if self.tag == None:
            return self.value        
        elif self.props == {}:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"

        
# Define ParentNode
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Missing tag")
        elif not self.children:
            raise ValueError("Missing children")
        else:
            children_html = "".join([child.to_html() for child in self.children])
            return f"<{self.tag}>{children_html}</{self.tag}>"


                         
