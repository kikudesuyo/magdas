init:
	cd backend && uv sync
	cd frontend && npm install

be-dev:
	cd backend && uv run inv server

fe-dev:
	cd frontend && npm run dev


up:
	docker-compose up -d --build

down:
		docker-compose down