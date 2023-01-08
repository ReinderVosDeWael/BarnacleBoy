from pathlib import Path
from typing import Union


class MermaidBase:
    def save_html(self, filename: Union[str, Path]) -> None:
        filename = Path(filename)
        content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Barnacle Boy</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@9.3.0/dist/mermaid.min.js"></script>
</head>

<body>
    <div class='mermaid'>
        {str(self)}
    </div>  
</body>
</html>      
        """

        with open(filename, "w") as file:
            file.write(content)
