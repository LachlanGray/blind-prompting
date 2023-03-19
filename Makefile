
build:
	docker build -t langchain -q .

start: 
	docker run -e OPENAI_API_KEY=$(OPENAI_API_KEY) \
	--name ai_box -d langchain

stop:
	docker stop ai_box
	docker rm ai_box

tests: build
	# make run val=name_of_function_in_tests.py
	docker cp blind_prompt ai_box:/
	docker exec ai_box python3 -c "from blind_prompt import tests; tests.$(test)()"

	
