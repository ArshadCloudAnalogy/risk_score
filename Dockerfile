FROM public.ecr.aws/lambda/python:3.11 AS build
WORKDIR /opt

# Copy and install Python dependencies into /opt/python
COPY requirements.txt .
RUN yum -y update \
 && yum -y install gcc gcc-c++ make git \
 && pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt --target /opt/python \
 && yum -y remove gcc gcc-c++ make git \
 && yum -y clean all \
 && rm -rf /var/cache/yum

#############################
# Stage 2: Final runtime image
#############################
FROM public.ecr.aws/lambda/python:3.11

# Copy dependencies from build stage
COPY --from=build /opt/python /opt/python

# Copy your Lambda function/app code into the task root
WORKDIR ${LAMBDA_TASK_ROOT}
COPY . .

# Optional: expose for local 'docker run' testing (Lambda Runtime API listens on 8080)
EXPOSE 8080

# IMPORTANT: Set the Lambda handler (module.function)
# Example expects a file `main.py` with `handler = Mangum(app)` inside.
CMD ["main.handler"]
