import * as vscode from 'vscode';
import * as path from 'path';

export function activate(context: vscode.ExtensionContext) {
    // Command to run the current CMRA file
    let runDisposable = vscode.commands.registerCommand('cmra.runFile', (uri?: vscode.Uri) => {
        // Find the file to run (either from context menu or active editor)
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
        
        // Wrap path in quotes to handle spaces
        terminal.sendText(`cmra "${filePath}"`);
    });

    // Command to start the REPL
    let replDisposable = vscode.commands.registerCommand('cmra.startRepl', () => {
        const terminal = vscode.window.createTerminal(`CMRA REPL`);
        terminal.show();
        terminal.sendText(`cmra repl`);
    });

    context.subscriptions.push(runDisposable);
    context.subscriptions.push(replDisposable);
}

export function deactivate() {}
