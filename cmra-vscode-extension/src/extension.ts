import * as vscode from 'vscode';

type TemplateContext = {
    line: number;
    name?: string;
    expected?: string;
    found?: string;
};

function pickRandom<T>(items: T[]): T {
    return items[Math.floor(Math.random() * items.length)];
}

function fillTemplate(template: string, ctx: TemplateContext): string {
    return template
        .replaceAll('{line}', String(ctx.line))
        .replaceAll('{name}', ctx.name ?? '')
        .replaceAll('{expected}', ctx.expected ?? '')
        .replaceAll('{found}', ctx.found ?? '');
}

function psQuote(value: string): string {
    return `"${value.replace(/`/g, '``').replace(/"/g, '`"')}"`;
}

function normalizeExecPath(raw: string | undefined): string {
    const value = (raw ?? 'python -m cmra').trim();
    const legacy = value.toLowerCase();

    if (!value || legacy === 'cmra' || legacy === 'cmra.exe' || legacy === '.\\cmra' || legacy === './cmra') {
        return 'python -m cmra';
    }

    return value;
}

const FIRE_MESSAGES = {
    undefinedVar: [
        "Line {line}: '{name}' is but a myth in this realm.\nHint: Bind it before you attempt to command it. 🐉",
        "Line {line}: The dragon searched for '{name}'... but found only ashes.\nHint: Use 'bind' to summon it into existence. 🔥",
        "Line {line}: '{name}' has not been bound to the dragon's will.\nHint: Bind it before invoking its name. 🐲",
        "Line {line}: No sigil named '{name}' answers your call.\nHint: Forge it first with 'bind'."
    ],
    missingConditionColon: [
        "Line {line}: The sniff incantation is incomplete.\nHint: Add ':' after the condition."
    ],
    missingPrintExpression: [
        "Line {line}: A roar with no words shakes only silence.\nHint: Add an expression after 'roar'."
    ],
    missingAssignmentValue: [
        "Line {line}: This binding ritual has no offering.\nHint: Add a value after 'bind'."
    ],
    wrongAssignmentOperator: [
        "Line {line}: Fire Dragon rejects '=' in this chant.\nHint: Use 'bind' for assignments in .cmra files."
    ],
    unknownCommand: [
        "Line {line}: The dragon does not recognize '{found}'.\nHint: Use known runes like bind, roar, sniff, dive, or soar."
    ],
    unmatchedBraces: [
        "Line {line}: The flame-circle of braces is unbalanced.\nHint: Check that every '{' has a matching '}'."
    ]
};

const SHADOW_MESSAGES = {
    undefinedVar: [
        "Line {line}: Undefined variable '{name}'.\nHint: Initialize it with '=' before using it.",
        "Line {line}: '{name}' was referenced before assignment.\nHint: Use '{name} = ...' first.",
        "Line {line}: Name '{name}' does not exist in scope.\nHint: Define it using '='."
    ],
    missingConditionColon: [
        "Line {line}: Invalid check syntax.\nHint: Add ':' after the condition."
    ],
    missingPrintExpression: [
        "Line {line}: 'print' requires an expression.\nHint: Example: print x + 1"
    ],
    missingAssignmentValue: [
        "Line {line}: Assignment is missing a value.\nHint: Use: {name} = <expression>"
    ],
    wrongAssignmentOperator: [
        "Line {line}: Unexpected 'bind' in .cmrash.\nHint: Use '=' for assignments."
    ],
    unknownCommand: [
        "Line {line}: Unknown command '{found}'.\nHint: Use '=', print, check, or reverse."
    ],
    unmatchedBraces: [
        "Line {line}: Unmatched braces detected.\nHint: Ensure every '{' has a closing '}'."
    ]
};

export function activate(context: vscode.ExtensionContext) {
    // Command to run the current CMRA file
    let runDisposable = vscode.commands.registerCommand('cmra.runFile', (uri?: vscode.Uri) => {
        let filePath = '';
        if (uri && uri.fsPath) {
            filePath = uri.fsPath;
        } else if (vscode.window.activeTextEditor) {
            filePath = vscode.window.activeTextEditor.document.fileName;
        }

        if (!filePath) {
            vscode.window.showErrorMessage('No CMRA file is currently open to run.');
            return;
        }

        // Only run .cmra or .cmrash files
        if (!filePath.endsWith('.cmra') && !filePath.endsWith('.cmrash')) {
            vscode.window.showErrorMessage('This file is not a valid CMRA file (.cmra or .cmrash).');
            return;
        }

        // Create or show terminal
        const terminal = vscode.window.createTerminal(`CMRA Run`);
        terminal.show();
        
        const config = vscode.workspace.getConfiguration('cmra');
        const execPath = normalizeExecPath(config.get<string>('executablePath', 'python -m cmra'));
        const quotedFile = psQuote(filePath);
        const runCommand = `${execPath} ${quotedFile}`;
        
        // Timeout prevents CommandNotFoundException when venv is busy activating
        setTimeout(() => {
            terminal.sendText(runCommand);
        }, 800);
    });

    // Command to start the REPL
    let replDisposable = vscode.commands.registerCommand('cmra.startRepl', () => {
        const terminal = vscode.window.createTerminal(`CMRA REPL`);
        terminal.show();
        const config = vscode.workspace.getConfiguration('cmra');
        const execPath = normalizeExecPath(config.get<string>('executablePath', 'python -m cmra'));
        setTimeout(() => {
            terminal.sendText(`${execPath} repl`);
        }, 800);
    });

    // ---- THEMATIC DIAGNOSTICS (STATIC ANALYZER) ----
    const diagnosticCollection = vscode.languages.createDiagnosticCollection('cmra');
    context.subscriptions.push(diagnosticCollection);

    function updateDiagnostics(document: vscode.TextDocument) {
        if (!document.fileName.endsWith('.cmra') && !document.fileName.endsWith('.cmrash')) return;
        
        const isFire = document.fileName.endsWith('.cmra');
        const msgBank = isFire ? FIRE_MESSAGES : SHADOW_MESSAGES;
        const text = document.getText();
        const lines = text.split(/\r?\n/);
        const diagnostics: vscode.Diagnostic[] = [];
        const boundVariables = new Set<string>();
        const keywords = isFire
            ? new Set(['murmur', 'bind', 'sniff', 'roar', 'dive', 'soar', 'check', 'print', 'reverse'])
            : new Set(['check', 'print', 'reverse', 'murmur']);
        const commandHead = isFire
            ? new Set(['sniff', 'check', 'roar', 'print', 'dive', 'soar'])
            : new Set(['check', 'print', 'reverse']);

        let braceBalance = 0;

        const pushDiag = (line: number, start: number, end: number, template: string, ctx: TemplateContext) => {
            diagnostics.push(
                new vscode.Diagnostic(
                    new vscode.Range(new vscode.Position(line, start), new vscode.Position(line, end)),
                    fillTemplate(template, ctx),
                    vscode.DiagnosticSeverity.Error
                )
            );
        };

        for (let i = 0; i < lines.length; i++) {
            const rawLine = lines[i];
            const line = rawLine.trim();
            if (!line || line.startsWith('murmur') || line.startsWith(';')) continue;

            const opens = (rawLine.match(/\{/g) || []).length;
            const closes = (rawLine.match(/\}/g) || []).length;
            braceBalance += opens - closes;

            if (isFire) {
                // In Fire Dragon, only `bind` is valid assignment syntax.
                // Flag true assignment form (`name = value`) but allow comparisons like ==, <=, >=, != in conditions.
                const illegalFireAssignment = rawLine.match(/^\s*[a-zA-Z_]\w*\s*=\s*(?!=)/);
                if (illegalFireAssignment) {
                    const idx = rawLine.indexOf('=');
                    pushDiag(i, Math.max(0, idx), Math.max(0, idx + 1), pickRandom(msgBank.wrongAssignmentOperator), { line: i + 1 });
                    continue;
                }
            }
            if (!isFire && /\bbind\b/.test(line)) {
                const idx = rawLine.indexOf('bind');
                pushDiag(i, Math.max(0, idx), Math.max(0, idx + 4), pickRandom(msgBank.wrongAssignmentOperator), { line: i + 1 });
                continue;
            }

            const fireAssign = rawLine.match(/^\s*([a-zA-Z_]\w*)\s+bind\b(.*)$/);
            const shadowAssign = rawLine.match(/^\s*([a-zA-Z_]\w*)\s*=\s*(.*)$/);
            const assign = isFire ? fireAssign : shadowAssign;

            if (assign) {
                const lhs = assign[1];
                const rhs = (assign[2] ?? '').trim();

                if (!rhs) {
                    const idx = rawLine.indexOf(lhs);
                    pushDiag(i, Math.max(0, idx), Math.max(0, idx + lhs.length), pickRandom(msgBank.missingAssignmentValue), {
                        line: i + 1,
                        name: lhs
                    });
                    continue;
                }

                const scrubbedRhs = rhs.replace(/"[^"]*"|'[^']*'/g, '');
                const rhsVars = scrubbedRhs.match(/\b([a-zA-Z_]\w*)\b/g) || [];
                for (const name of rhsVars) {
                    if (keywords.has(name) || boundVariables.has(name)) continue;
                    const idx = rawLine.indexOf(name);
                    pushDiag(i, Math.max(0, idx), Math.max(0, idx + name.length), pickRandom(msgBank.undefinedVar), {
                        line: i + 1,
                        name
                    });
                }

                boundVariables.add(lhs);
                continue;
            }

            const firstWord = line.match(/^([a-zA-Z_]\w*)/)?.[1] ?? '';

            if (firstWord === 'sniff' || firstWord === 'check') {
                if (!line.includes(':')) {
                    pushDiag(i, 0, rawLine.length || 1, pickRandom(msgBank.missingConditionColon), { line: i + 1 });
                    continue;
                }
            }

            if (firstWord === 'roar' || firstWord === 'print') {
                const expr = line.slice(firstWord.length).trim();
                if (!expr) {
                    pushDiag(i, 0, rawLine.length || 1, pickRandom(msgBank.missingPrintExpression), { line: i + 1 });
                    continue;
                }
            }

            if (firstWord && !commandHead.has(firstWord)) {
                if (line !== '{' && line !== '}') {
                    const idx = rawLine.indexOf(firstWord);
                    pushDiag(i, Math.max(0, idx), Math.max(0, idx + firstWord.length), pickRandom(msgBank.unknownCommand), {
                        line: i + 1,
                        found: firstWord
                    });
                    continue;
                }
            }
            
            // Identify used token variables for non-assignment statements.
            const scrubbed = rawLine.replace(/"[^"]*"|'[^']*'/g, '');
            const tokens = scrubbed.match(/\b([a-zA-Z_]\w*)\b/g);
            if (tokens) {
                for (const t of tokens) {
                    if (keywords.has(t)) continue;
                    if (!boundVariables.has(t)) {
                        const idx = rawLine.indexOf(t);
                        pushDiag(i, Math.max(0, idx), Math.max(0, idx + t.length), pickRandom(msgBank.undefinedVar), {
                            line: i + 1,
                            name: t
                        });
                    }
                }
            }
        }

        if (braceBalance !== 0) {
            const line = Math.max(0, lines.length - 1);
            pushDiag(line, 0, (lines[line]?.length || 1), pickRandom(msgBank.unmatchedBraces), { line: line + 1 });
        }

        diagnosticCollection.set(document.uri, diagnostics);
    }
    
    vscode.workspace.onDidChangeTextDocument(e => updateDiagnostics(e.document), null, context.subscriptions);
    vscode.workspace.onDidOpenTextDocument(updateDiagnostics, null, context.subscriptions);
    if (vscode.window.activeTextEditor) {
        updateDiagnostics(vscode.window.activeTextEditor.document);
    }

    // Hover Provider for keyword documentation
    let hoverProvider = vscode.languages.registerHoverProvider('cmra', {
        provideHover(document, position, token) {
            const range = document.getWordRangeAtPosition(position);
            const word = document.getText(range);

            const docs: { [key: string]: string } = {
                'murmur': '**Comment**: The dragon ignores this line. Use it for notes.',
                'bind': '**Assignment**: Binds a value to the name on the left.',
                'sniff': '**Conditional**: Checks the condition and executes the block if true.',
                'roar': '**Print**: Outputs the expression result to the console.',
                'dive': '**Forward Direction**: Sets execution to move normally (down).',
                'soar': '**Backward Direction**: Flips execution to move upwards.',
                'check': '**Debug**: Verification command.',
                'print': '**Alias**: Outputs expression results.'
            };

            if (docs[word]) {
                return new vscode.Hover(new vscode.MarkdownString(docs[word]));
            }
            return undefined;
        }
    });

    context.subscriptions.push(runDisposable);
    context.subscriptions.push(replDisposable);
    context.subscriptions.push(hoverProvider);
}

export function deactivate() {}
