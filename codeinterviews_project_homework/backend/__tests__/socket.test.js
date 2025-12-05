const { io: Client } = require('socket.io-client');
const { server, sessions } = require('../server');

describe('Socket.IO Tests', () => {
  let clientSocket;
  let runningServer;
  let port;

  beforeAll((done) => {
    runningServer = server.listen(0, () => {
      port = runningServer.address().port;
      done();
    });
  });

  afterAll((done) => {
    runningServer.close(done);
  });

  beforeEach((done) => {
    clientSocket = new Client(`http://localhost:${port}`);
    clientSocket.on('connect', done);
  });

  afterEach(() => {
    clientSocket.close();
  });

  it('should join a session and receive code', (done) => {
    const sessionId = 'test-session';
    sessions.set(sessionId, { code: 'console.log("hello");', participants: new Set() });

    clientSocket.emit('join', sessionId);

    clientSocket.on('code', (code) => {
      expect(code).toBe('console.log("hello");');
      done();
    });
  });

  it('should receive an error for a non-existent session', (done) => {
    clientSocket.emit('join', 'non-existent-session');

    clientSocket.on('error', (error) => {
      expect(error).toBe('Session not found');
      done();
    });
  });
});
