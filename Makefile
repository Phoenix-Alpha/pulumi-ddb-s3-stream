DIST_DIR=./dist
LAMBDA_FNAME=lambda.zip
LAYER_FNAME=layer.zip
LAMBDA_PATH=${DIST_DIR}/${LAMBDA_FNAME}
LAYER_PATH=${DIST_DIR}/${LAYER_FNAME}
REQUIREMENTS_DIR=./requirements

lambda:
	zip -9 ${LAMBDA_PATH} handler.py

# TODO: use Docker to install requirements via lambci/python3.7 image
# Otherwise we can't guarantee package compatibility with Lambda

# NB: layer zip must contain "python" folder, that's why it's hard-coded
layer:
	python3 -m pip install \
		--requirement ${REQUIREMENTS_DIR}/lambda.txt \
		--target ${DIST_DIR}/python
	cd ${DIST_DIR} && zip -r9 ${LAYER_FNAME} python