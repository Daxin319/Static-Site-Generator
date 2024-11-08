class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag == other.tag and 
                self.value == other.value and 
                self.children == other.children and 
                self.props == other.props)

    def to_html(self):
        raise NotImplementedError
        #children will overwrite this method

    #function to convert properties attribute to proper html format
    def props_to_html(self):
        html_string = ""
        for key in self.props:
            html_string += f' {key}="{self.props[key]}"'
        return html_string
    
    def __repr__(self):
        parts = [repr(self.tag)]
        if self.value is not None:
            parts.append(repr(self.value))
        if self.children:
            children_repr = "[" + ", ".join(repr(child) for child in self.children) + "]"
            parts.append(children_repr)
        if self.props:
            parts.append(repr(self.props))
        return f'HTMLNode({", ".join(parts)})'
    
    #function to convert node to html format
    def to_html(self):
        if not self.tag:
            return str(self.value)
    
        props_string = self.props_to_html() if self.props else ""
    
        if self.tag == "img":
            return f"<{self.tag}{props_string} />"
    
        children_html = ""
        if self.children:
            for child in self.children:
                children_html += child.to_html()
    
        value_string = str(self.value) if self.value is not None else ""
        return f"<{self.tag}{props_string}>{value_string}{children_html}</{self.tag}>"