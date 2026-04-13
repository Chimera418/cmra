# CMRA Esoteric Language

![CMRA Theme](https://img.shields.io/badge/Syntax-Dragon_Flavored-red)
![Version](https://img.shields.io/badge/version-1.1.0-blue)

**CMRA Esoteric Language** brings syntax highlighting, useful snippets, and local run support for the `CMRA` programming language to your favorite IDEs like VS Code and Cursor.

## 🔥 Features
- **Syntax Highlighting**: Beautiful and accurate tokenization for both Fire Dragon (`.cmra`) and Shadow Dragon (`.cmrash`) dialects.
- **Run Support**: Right-click or use the Command Palette to execute your dragon code directly in the integrated terminal.
- **Snippets**: Type `hello`, `cond`, or `loop` to instantly scaffold patterns for both dialects. 
- **Themed Diagnostics**: Static analyzer with dragon-style errors for `.cmra` and concise technical errors for `.cmrash`.

## ⚡ Installation & Usage

### 1. The Extension
Get the latest version straight from the [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=Chimera418.cmra-esolang) or [Open VSX Registry](https://open-vsx.org/vscode/item?itemName=Chimera418.cmra-esolang) by clicking the links or searching for **CMRA Esoteric Language**. 

*Alternatively, you can download the latest `.vsix` file from the [GitHub Releases](https://github.com/Chimera418/cmra/releases) and install it manually.*

### 2. The Python CLI
To use the "Run CMRA File" command within your editor, install CMRA in the Python environment you actually use for development:
```bash
pip install cmra
```

The extension run command defaults to:
```bash
python -m cmra "<file>"
```
This avoids relying on a globally available `cmra` binary on PATH.

## 📖 Extension Commands

- `CMRA: Run File`: Executes the currently active `.cmra` or `.cmrash` file using the installed interpreter.

## ⚙️ Configuration


- `cmra.executablePath` (default: `python -m cmra`)
	- Use this when run fails in PowerShell due to PATH/venv issues.
	- Examples:
		- `python -m cmra`
		- `py -m cmra`
		- `C:\\path\\to\\venv\\Scripts\\cmra.exe`
		- `.\\cmra.bat`

## 🧯 Diagnostics & Error Variants

The extension randomizes message text within each error family so repeated issues do not feel repetitive.
Messages are themed differently for Fire Dragon (`.cmra`) and Shadow Dragon (`.cmrash`).

### Fire Dragon (`.cmra`) error families

1. Undefined variable
- `Line 4: 'x' is but a myth in this realm.`
	`Hint: Bind it before you attempt to command it. 🐉`
- `Line 4: The dragon searched for 'x'... but found only ashes.`
	`Hint: Use 'bind' to summon it into existence. 🔥`

2. Missing condition colon (`sniff` / `check`)
- `Line 3: The sniff incantation is incomplete.`
	`Hint: Add ':' after the condition.`

3. Missing print expression (`roar`)
- `Line 7: A roar with no words shakes only silence.`
	`Hint: Add an expression after 'roar'.`

4. Missing assignment value (`bind`)
- `Line 2: This binding ritual has no offering.`
	`Hint: Add a value after 'bind'.`

5. Wrong assignment operator in `.cmra`
- `Line 5: Fire Dragon rejects '=' in this chant.`
	`Hint: Use 'bind' for assignments in .cmra files.`

6. Unknown command
- `Line 6: The dragon does not recognize 'ignite'.`
	`Hint: Use known runes like bind, roar, sniff, dive, or soar.`

7. Unmatched braces
- `Line 12: The flame-circle of braces is unbalanced.`
	`Hint: Check that every '{' has a matching '}'.`

### Shadow Dragon (`.cmrash`) error families

1. Undefined variable
- `Line 4: Undefined variable 'x'.`
	`Hint: Initialize it with '=' before using it.`
- `Line 4: 'x' was referenced before assignment.`
	`Hint: Use 'x = ...' first.`

2. Missing condition colon (`check`)
- `Line 3: Invalid check syntax.`
	`Hint: Add ':' after the condition.`

3. Missing print expression (`print`)
- `Line 7: 'print' requires an expression.`
	`Hint: Example: print x + 1`

4. Missing assignment value (`=`)
- `Line 2: Assignment is missing a value.`
	`Hint: Use: x = <expression>`

5. Wrong assignment keyword in `.cmrash`
- `Line 5: Unexpected 'bind' in .cmrash.`
	`Hint: Use '=' for assignments.`

6. Unknown command
- `Line 6: Unknown command 'ignite'.`
	`Hint: Use '=', print, check, or reverse.`

7. Unmatched braces
- `Line 12: Unmatched braces detected.`
	`Hint: Ensure every '{' has a closing '}'.`

`ERROR_MESSAGES.md` is kept as the canonical source for internal maintenance and cross-doc syncing.

## 🔗 Documentation

- 🌐 **Website**: [cmra-esolang.vercel.app](https://cmra-esolang.vercel.app/index.html)
- 🔥 **Playground**: [Try it live online](https://cmra-esolang.vercel.app/playground.html)
- 📖 **User Guide**: [Documentation & Pitfalls Guide](https://cmra-esolang.vercel.app/guide.html) (also available on [GitHub](https://github.com/Chimera418/cmra/blob/main/GUIDE.md))
- 🐙 **GitHub Repository**: [Chimera418/cmra](https://github.com/Chimera418/cmra)

---

*May your code burn bright and your loops reverse true!* 🐉🔥
