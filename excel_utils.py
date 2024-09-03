import pandas as pd 
def unmerge_cells(df):
    return df.ffill(axis=0)  # Simple forward-fill example

def concatenate_requirements(df):
    concatenated_requirements = []
    section_hierarchy = {}
    current_requirement = ""

    for index, row in df.iterrows():
        section = row.get('section', '')
        requirement = row.get('requirement', '')

        if pd.notna(requirement):
            level = section.count('.')
            section_hierarchy[level] = requirement
            current_requirement = " ".join(
                [section_hierarchy[i] for i in range(1, level + 1) if i in section_hierarchy]
            )
            concatenated_requirements.append(current_requirement)
        else:
            concatenated_requirements.append(current_requirement)

    df['concatenated_requirement'] = concatenated_requirements
    return df

def save_to_excel(df):
    from io import BytesIO
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return output
