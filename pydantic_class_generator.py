def generate_pydantic_model(class_name: str, fields: dict) -> str:
    """
    Generate a Pydantic model class definition as a string.

    :param class_name: Name of the class to generate.
    :param fields: Dictionary where key = field name, value = field type.
    :return: String representing the Python class.
    """
    lines = ["from pydantic import BaseModel", "", f"class {class_name}(BaseModel):"]

    if not fields:
        lines.append("    pass")
    else:
        for field_name, field_type in fields.items():
            lines.append(f"    {field_name}: {field_type}")

    return "\n".join(lines)


if __name__ == "__main__":
    # Example usage
    class_name = input("Enter class name: ")
    print("Enter fields in format name:type (e.g., name:str, age:int). Type 'done' to finish.")

    fields = {}
    while True:
        field_input = input("Field: ").strip()
        if field_input.lower() == "done":
            break
        if ":" in field_input:
            name, type_ = field_input.split(":", 1)
            fields[name.strip()] = type_.strip()
        else:
            print("❌ Invalid format. Use name:type (e.g., email:str)")

    model_code = generate_pydantic_model(class_name, fields)
    print("\n✅ Generated Pydantic Model:\n")
    print(model_code)

    # Optional: save to file
    with open(f"{class_name.lower()}.py", "w") as f:
        f.write(model_code)
    print(f"\n💾 Saved to {class_name.lower()}.py")



#Example
# Enter class name: Customer
# Enter fields in format name:type (e.g., name:str, age:int). Type 'done' to finish.
# Field: name:str
# Field: email:str
# Field: age:int
# Field: is_active:bool
# Field: done