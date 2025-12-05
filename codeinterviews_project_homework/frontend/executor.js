self.onmessage = (e) => {
    try {
        const result = new Function(e.data)();
        self.postMessage({ result: result !== undefined ? String(result) : '' });
    } catch (error) {
        self.postMessage({ error: error.stack });
    }
};
