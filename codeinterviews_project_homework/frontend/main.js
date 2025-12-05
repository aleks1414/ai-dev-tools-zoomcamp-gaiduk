import * as monaco from 'monaco-editor';
import { io } from 'socket.io-client';

// Monaco Editor setup with CDN workers
self.MonacoEnvironment = {
    getWorkerUrl: function (moduleId, label) {
        if (label === 'json') {
            return './monaco-editor/esm/vs/language/json/json.worker.js';
        }
        if (label === 'css' || label === 'scss' || label === 'less') {
            return './monaco-editor/esm/vs/language/css/css.worker.js';
        }
        if (label === 'html' || label === 'handlebars' || label === 'razor') {
            return './monaco-editor/esm/vs/language/html/html.worker.js';
        }
        if (label === 'typescript' || label === 'javascript') {
            return './monaco-editor/esm/vs/language/typescript/ts.worker.js';
        }
        return './monaco-editor/esm/vs/editor/editor.worker.js';
    }
};

const editorContainer = document.getElementById('editor-container');
const outputContainer = document.getElementById('output');

const getSessionId = () => {
    const path = window.location.pathname;
    const parts = path.split('/');
    if (parts.length > 1 && parts[1]) {
        return parts[1];
    }
    return null;
};

const createSession = async () => {
    const res = await fetch('/api/sessions', { method: 'POST' });
    const { sessionId } = await res.json();
    window.history.pushState({}, '', `/${sessionId}`);
    return sessionId;
};

const main = async () => {
    let sessionId = getSessionId();
    if (!sessionId) {
        sessionId = await createSession();
    }

    const socket = io();

    const editor = monaco.editor.create(editorContainer, {
        value: '// Welcome to the Code Interview Editor!\n// Press Ctrl+Enter (or Cmd+Enter) to execute JavaScript code\n\nconsole.log("Hello, World!");',
        language: 'javascript',
        theme: 'vs-dark',
        automaticLayout: true,
    });

    const languageSelector = document.createElement('select');
    languageSelector.style.position = 'absolute';
    languageSelector.style.top = '10px';
    languageSelector.style.right = '10px';
    languageSelector.style.zIndex = '100';
    languageSelector.style.padding = '5px';
    languageSelector.style.backgroundColor = '#2d2d30';
    languageSelector.style.color = '#cccccc';
    languageSelector.style.border = '1px solid #464647';
    document.body.appendChild(languageSelector);

    const languages = ['javascript', 'python', 'cpp'];
    languages.forEach(lang => {
        const option = document.createElement('option');
        option.value = lang;
        option.textContent = lang;
        languageSelector.appendChild(option);
    });

    languageSelector.addEventListener('change', (e) => {
        monaco.editor.setModelLanguage(editor.getModel(), e.target.value);
    });

    socket.emit('join', sessionId);

    socket.on('code', (code) => {
        const currentCode = editor.getValue();
        if (currentCode !== code) {
            editor.setValue(code);
        }
    });

    editor.onDidChangeModelContent(() => {
        const code = editor.getValue();
        socket.emit('codeChange', code);
    });

    const executeCode = (code) => {
        try {
            // Simple JavaScript execution
            const originalLog = console.log;
            const logs = [];
            console.log = (...args) => {
                logs.push(args.map(arg => 
                    typeof arg === 'object' ? JSON.stringify(arg, null, 2) : String(arg)
                ).join(' '));
            };
            
            const result = new Function(code)();
            console.log = originalLog;
            
            let output = '';
            if (logs.length > 0) {
                output += logs.join('\n');
            }
            if (result !== undefined) {
                output += (output ? '\n' : '') + 'Result: ' + (typeof result === 'object' ? JSON.stringify(result, null, 2) : String(result));
            }
            
            outputContainer.textContent = output || 'Code executed successfully (no output)';
        } catch (error) {
            outputContainer.textContent = 'Error: ' + error.message;
        }
    };
    
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => {
        executeCode(editor.getValue());
    });

};

main().catch(console.error);
