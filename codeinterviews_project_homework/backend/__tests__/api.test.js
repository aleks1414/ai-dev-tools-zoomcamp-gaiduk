const request = require('supertest');
const { app, server, sessions } = require('../server');

describe('API Tests', () => {
  let runningServer;
  beforeAll((done) => {
    runningServer = server.listen(0, done);
  });

  afterAll((done) => {
    runningServer.close(done);
  });

  it('should create a new session', async () => {
    const res = await request(app).post('/api/sessions');
    expect(res.statusCode).toEqual(201);
    expect(res.body).toHaveProperty('sessionId');
    const { sessionId } = res.body;
    expect(sessions.has(sessionId)).toBe(true);
  });

  it('should join an existing session', async () => {
    const createRes = await request(app).post('/api/sessions');
    const { sessionId } = createRes.body;

    const joinRes = await request(app).get(`/api/sessions/${sessionId}`);
    expect(joinRes.statusCode).toEqual(200);
    expect(joinRes.body).toHaveProperty('sessionId', sessionId);
  });

  it('should return 404 for a non-existent session', async () => {
    const res = await request(app).get('/api/sessions/non-existent-session');
    expect(res.statusCode).toEqual(404);
  });

  it('should return 200 for health check', async () => {
    const res = await request(app).get('/api/health');
    expect(res.statusCode).toEqual(200);
    expect(res.text).toBe('OK');
  });
});
