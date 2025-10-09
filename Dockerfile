FROM public.ecr.aws/lambda/python:3.11

# If you used a build stage for deps, copy them here
# COPY --from=build /opt/python /opt/python

# Install requirements directly if you prefer single stage:
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code to Lambda task root
WORKDIR ${LAMBDA_TASK_ROOT}
COPY . .

# No custom ENTRYPOINT. Lambda provides it.
CMD ["main.handler"]
