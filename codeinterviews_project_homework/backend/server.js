const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const { v4: uuidv4 } = require('uuid');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: '*',
  },
});

const sessions = new Map();

app.use(express.json());

app.post('/api/sessions', (req, res) => {
  const sessionId = uuidv4();
  sessions.set(sessionId, {
    code: '',
    participants: new Set(),
  });
  res.status(201).json({ sessionId });
});

app.get('/api/sessions/:sessionId', (req, res) => {
  const { sessionId } = req.params;
  if (sessions.has(sessionId)) {
    res.status(200).json({ sessionId });
  } else {
    res.status(404).json({ error: 'Session not found' });
  }
});

app.get('/api/health', (req, res) => {
  res.status(200).send('OK');
});

io.on('connection', (socket) => {
  console.log('a user connected');

  socket.on('join', (sessionId) => {
    if (sessions.has(sessionId)) {
      socket.join(sessionId);
      const session = sessions.get(sessionId);
      session.participants.add(socket.id);
      socket.emit('code', session.code);

      socket.on('codeChange', (newCode) => {
        session.code = newCode;
        socket.to(sessionId).emit('code', newCode);
      });

      socket.on('cursorChange', (cursor) => {
        socket.to(sessionId).emit('cursor', { ...cursor, userId: socket.id });
      });

      socket.on('selectionChange', (selection) => {
        socket.to(sessionId).emit('selection', { ...selection, userId: socket.id });
      });

      socket.on('cursorChange', (cursor) => {
        socket.to(sessionId).emit('cursor', { ...cursor, userId: socket.id });
      });

      socket.on('selectionChange', (selection) => {
        socket.to(sessionId).emit('selection', { ...selection, userId: socket.id });
      });

      socket.on('disconnect', () => {
        console.log('user disconnected');
        session.participants.delete(socket.id);
        if (session.participants.size === 0) {
          sessions.delete(sessionId);
        }
      });
    } else {
      socket.emit('error', 'Session not found');
    }
  });
});

const PORT = process.env.PORT || 3000;
if (require.main === module) {
  server.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
  });
}

module.exports = { app, server, sessions };
