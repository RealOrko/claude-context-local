"""Sindarin-specific tree-sitter based chunker."""

from typing import Any, Dict, Set

from chunking.base_chunker import LanguageChunker


class SindarinChunker(LanguageChunker):
    """Sindarin-specific chunker using tree-sitter.

    Sindarin is a systems programming language with:
    - Native C interop via `native fn` declarations
    - Struct-based OOP with instance and static methods
    - Strong static typing
    - Block syntax using `=>`
    """

    def __init__(self):
        super().__init__('sindarin')

    def _get_splittable_node_types(self) -> Set[str]:
        """Sindarin-specific splittable node types."""
        return {
            'function_declaration',
            'native_function_declaration',
            'static_function_declaration',
            'struct_declaration',
            'type_declaration',
        }

    def extract_metadata(self, node: Any, source: bytes) -> Dict[str, Any]:
        """Extract Sindarin-specific metadata."""
        metadata = {'node_type': node.type}

        # Extract name from the 'name' field
        name_node = node.child_by_field_name('name')
        if name_node:
            metadata['name'] = self.get_node_text(name_node, source)

        # Extract return type for functions
        return_type_node = node.child_by_field_name('return_type')
        if return_type_node:
            metadata['return_type'] = self.get_node_text(return_type_node, source)

        # Extract parameters for functions
        params_node = node.child_by_field_name('parameters')
        if params_node:
            param_names = []
            for child in params_node.children:
                if child.type == 'parameter':
                    param_name_node = child.child_by_field_name('name')
                    if param_name_node:
                        param_names.append(self.get_node_text(param_name_node, source))
            if param_names:
                metadata['parameters'] = param_names
                metadata['param_count'] = len(param_names)

        # Check for visibility modifiers
        modifier_node = node.child_by_field_name('modifier')
        if modifier_node:
            metadata['visibility'] = self.get_node_text(modifier_node, source)

        # Check if it's a native function
        if node.type == 'native_function_declaration':
            metadata['is_native'] = True

        # Check if it's a static function
        if node.type == 'static_function_declaration':
            metadata['is_static'] = True

        # For structs, extract field information
        if node.type == 'struct_declaration':
            body_node = node.child_by_field_name('body')
            if body_node:
                fields = []
                methods = []
                static_methods = []
                for child in body_node.children:
                    if child.type == 'field_declaration':
                        field_name = child.child_by_field_name('name')
                        if field_name:
                            fields.append(self.get_node_text(field_name, source))
                    elif child.type == 'function_declaration':
                        method_name = child.child_by_field_name('name')
                        if method_name:
                            methods.append(self.get_node_text(method_name, source))
                    elif child.type == 'static_function_declaration':
                        method_name = child.child_by_field_name('name')
                        if method_name:
                            static_methods.append(self.get_node_text(method_name, source))

                if fields:
                    metadata['fields'] = fields
                if methods:
                    metadata['methods'] = methods
                if static_methods:
                    metadata['static_methods'] = static_methods

        # Check for decorators (for native functions)
        decorators = []
        for child in node.children:
            if child.type == 'decorator':
                decorators.append(self.get_node_text(child, source))
        if decorators:
            metadata['decorators'] = decorators

        return metadata
