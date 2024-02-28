GitHub - openai/openai-python: The official Python library for the OpenAI API

Skip to content

Toggle navigation

          Sign in
        

 

        Product
        

Actions
        Automate any workflow
      

Packages
        Host and manage packages
      

Security
        Find and fix vulnerabilities
      

Codespaces
        Instant dev environments
      

Copilot
        Write better code with AI
      

Code review
        Manage code changes
      

Issues
        Plan and track work
      

Discussions
        Collaborate outside of code
      

Explore

      All features

    

      Documentation

    

      GitHub Skills

    

      Blog

    

        Solutions
        

For

      Enterprise

    

      Teams

    

      Startups

    

      Education

    

By Solution

      CI/CD &amp; Automation

    

      DevOps

    

      DevSecOps

    

Resources

      Learning Pathways

    

      White papers, Ebooks, Webinars

    

      Customer Stories

    

      Partners

    

        Open Source
        

GitHub Sponsors
        Fund open source developers
      

The ReadME Project
        GitHub community articles
      

Repositories

      Topics

    

      Trending

    

      Collections

    

Pricing

Search or jump to...

Search code, repositories, users, issues, pull requests...

 

        Search
      

Clear
 

 

              Search syntax tips
 

        Provide feedback
      

 
We read every piece of feedback, and take your input very seriously.

Include my email address so I can be contacted

     Cancel

    Submit feedback

        Saved searches
      
Use saved searches to filter your results more quickly

 

Name

Query

            To see all available qualifiers, see our documentation.
          
 

     Cancel

    Create saved search

              Sign in
            

              Sign up
            

You signed in with another tab or window. Reload to refresh your session.
You signed out in another tab or window. Reload to refresh your session.
You switched accounts on another tab or window. Reload to refresh your session.
 

Dismiss alert

        openai
 
/

openai-python

Public

 

Notifications

 

Fork
    2.5k

 

          Star
 18.7k
  

        The official Python library for the OpenAI API
      

pypi.org/project/openai/

License

     Apache-2.0 license
    

18.7k
          stars
 

2.5k
          forks
 

Branches
 

Tags
 

Activity
 

 

          Star

  

 

Notifications

Code

Issues
62

Pull requests
8

Discussions

Actions

Security

Insights

 

 

Additional navigation options

 

          Code

          Issues

          Pull requests

          Discussions

          Actions

          Security

          Insights

 

openai/openai-python

This commit does not belong to any branch on this repository, and may belong to a fork outside of the repository.

   &nbsp;mainBranchesTagsGo to fileCodeFolders and filesNameNameLast commit messageLast commit dateLatest commit&nbsp;History363 Commits.devcontainer.devcontainer&nbsp;&nbsp;.github.github&nbsp;&nbsp;binbin&nbsp;&nbsp;examplesexamples&nbsp;&nbsp;src/openaisrc/openai&nbsp;&nbsp;teststests&nbsp;&nbsp;.gitignore.gitignore&nbsp;&nbsp;.python-version.python-version&nbsp;&nbsp;.release-please-manifest.json.release-please-manifest.json&nbsp;&nbsp;.stats.yml.stats.yml&nbsp;&nbsp;CHANGELOG.mdCHANGELOG.md&nbsp;&nbsp;CONTRIBUTING.mdCONTRIBUTING.md&nbsp;&nbsp;LICENSELICENSE&nbsp;&nbsp;README.mdREADME.md&nbsp;&nbsp;api.mdapi.md&nbsp;&nbsp;mypy.inimypy.ini&nbsp;&nbsp;noxfile.pynoxfile.py&nbsp;&nbsp;pyproject.tomlpyproject.toml&nbsp;&nbsp;release-please-config.jsonrelease-please-config.json&nbsp;&nbsp;requirements-dev.lockrequirements-dev.lock&nbsp;&nbsp;requirements.lockrequirements.lock&nbsp;&nbsp;View all filesRepository files navigationREADMEApache-2.0 licenseOpenAI Python API library

The OpenAI Python library provides convenient access to the OpenAI REST API from any Python 3.7+
application. The library includes type definitions for all request params and response fields,
and offers both synchronous and asynchronous clients powered by httpx.
It is generated from our OpenAPI specification with Stainless.
Documentation
The REST API documentation can be found on platform.openai.com. The full API of this library can be found in api.md.
Installation
ImportantThe SDK was rewritten in v1, which was released November 6th 2023. See the v1 migration guide, which includes scripts to automatically update your code.

pip install openai
Usage
The full API of this library can be found in api.md.
import os
from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-3.5-turbo",
)
While you can provide an api_key keyword argument,
we recommend using python-dotenv
to add OPENAI_API_KEY="My API Key" to your .env file
so that your API Key is not stored in source control.
Async usage
Simply import AsyncOpenAI instead of OpenAI and use await with each API call:
import os
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

async def main() -&gt; None:
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Say this is a test",
            }
        ],
        model="gpt-3.5-turbo",
    )

asyncio.run(main())
Functionality between the synchronous and asynchronous clients is otherwise identical.
Streaming Responses
We provide support for streaming responses using Server Side Events (SSE).
from openai import OpenAI

client = OpenAI()

stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Say this is a test"}],
    stream=True,
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")
The async client uses the exact same interface.
from openai import AsyncOpenAI

client = AsyncOpenAI()

async def main():
    stream = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Say this is a test"}],
        stream=True,
    )
    async for chunk in stream:
        print(chunk.choices[0].delta.content or "", end="")

asyncio.run(main())
Module-level client
ImportantWe highly recommend instantiating client instances instead of relying on the global client.

We also expose a global client instance that is accessible in a similar fashion to versions prior to v1.
import openai

# optional; defaults to `os.environ['OPENAI_API_KEY']`
openai.api_key = '...'

# all client options can be configured just like the `OpenAI` instantiation counterpart
openai.base_url = "https://..."
openai.default_headers = {"x-foo": "true"}

completion = openai.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "user",
            "content": "How do I output all files in a directory using Python?",
        },
    ],
)
print(completion.choices[0].message.content)
The API is the exact same as the standard client instance based API.
This is intended to be used within REPLs or notebooks for faster iteration, not in application code.
We recommend that you always instantiate a client (e.g., with client = OpenAI()) in application code because:

It can be difficult to reason about where client options are configured
It's not possible to change certain client options without potentially causing race conditions
It's harder to mock for testing purposes
It's not possible to control cleanup of network connections

Using types
Nested request parameters are TypedDicts. Responses are Pydantic models, which provide helper methods for things like:

Serializing back into JSON, model.model_dump_json(indent=2, exclude_unset=True)
Converting to a dictionary, model.model_dump(exclude_unset=True)

Typed requests and responses provide autocomplete and documentation within your editor. If you would like to see type errors in VS Code to help catch bugs earlier, set python.analysis.typeCheckingMode to basic.
Pagination
List methods in the OpenAI API are paginated.
This library provides auto-paginating iterators with each list response, so you do not have to request successive pages manually:
import openai

client = OpenAI()

all_jobs = []
# Automatically fetches more pages as needed.
for job in client.fine_tuning.jobs.list(
    limit=20,
):
    # Do something with job here
    all_jobs.append(job)
print(all_jobs)
Or, asynchronously:
import asyncio
import openai

client = AsyncOpenAI()

async def main() -&gt; None:
    all_jobs = []
    # Iterate through items across all pages, issuing requests as needed.
    async for job in client.fine_tuning.jobs.list(
        limit=20,
    ):
        all_jobs.append(job)
    print(all_jobs)

asyncio.run(main())
Alternatively, you can use the .has_next_page(), .next_page_info(), or .get_next_page() methods for more granular control working with pages:
first_page = await client.fine_tuning.jobs.list(
    limit=20,
)
if first_page.has_next_page():
    print(f"will fetch next page using these details: {first_page.next_page_info()}")
    next_page = await first_page.get_next_page()
    print(f"number of items we just fetched: {len(next_page.data)}")

# Remove `await` for non-async usage.
Or just work directly with the returned data:
first_page = await client.fine_tuning.jobs.list(
    limit=20,
)

print(f"next page cursor: {first_page.after}")  # =&gt; "next page cursor: ..."
for job in first_page.data:
    print(job.id)

# Remove `await` for non-async usage.
Nested params
Nested parameters are dictionaries, typed using TypedDict, for example:
from openai import OpenAI

client = OpenAI()

completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Can you generate an example json object describing a fruit?",
        }
    ],
    model="gpt-3.5-turbo-1106",
    response_format={"type": "json_object"},
)
File Uploads
Request parameters that correspond to file uploads can be passed as bytes, a PathLike instance or a tuple of (filename, contents, media type).
from pathlib import Path
from openai import OpenAI

client = OpenAI()

client.files.create(
    file=Path("input.jsonl"),
    purpose="fine-tune",
)
The async client uses the exact same interface. If you pass a PathLike instance, the file contents will be read asynchronously automatically.
Handling errors
When the library is unable to connect to the API (for example, due to network connection problems or a timeout), a subclass of openai.APIConnectionError is raised.
When the API returns a non-success status code (that is, 4xx or 5xx
response), a subclass of openai.APIStatusError is raised, containing status_code and response properties.
All errors inherit from openai.APIError.
import openai
from openai import OpenAI

client = OpenAI()

try:
    client.fine_tuning.jobs.create(
        model="gpt-3.5-turbo",
        training_file="file-abc123",
    )
except openai.APIConnectionError as e:
    print("The server could not be reached")
    print(e.__cause__)  # an underlying Exception, likely raised within httpx.
except openai.RateLimitError as e:
    print("A 429 status code was received; we should back off a bit.")
except openai.APIStatusError as e:
    print("Another non-200-range status code was received")
    print(e.status_code)
    print(e.response)
Error codes are as followed:

Status Code
Error Type

400
BadRequestError

401
AuthenticationError

403
PermissionDeniedError

404
NotFoundError

422
UnprocessableEntityError

429
RateLimitError

&gt;=500
InternalServerError

N/A
APIConnectionError

Retries
Certain errors are automatically retried 2 times by default, with a short exponential backoff.
Connection errors (for example, due to a network connectivity problem), 408 Request Timeout, 409 Conflict,
429 Rate Limit, and &gt;=500 Internal errors are all retried by default.
You can use the max_retries option to configure or disable retry settings:
from openai import OpenAI

# Configure the default for all requests:
client = OpenAI(
    # default is 2
    max_retries=0,
)

# Or, configure per-request:
client.with_options(max_retries=5).chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "How can I get the name of the current day in Node.js?",
        }
    ],
    model="gpt-3.5-turbo",
)
Timeouts
By default requests time out after 10 minutes. You can configure this with a timeout option,
which accepts a float or an httpx.Timeout object:
from openai import OpenAI

# Configure the default for all requests:
client = OpenAI(
    # 20 seconds (default is 10 minutes)
    timeout=20.0,
)

# More granular control:
client = OpenAI(
    timeout=httpx.Timeout(60.0, read=5.0, write=10.0, connect=2.0),
)

# Override per-request:
client.with_options(timeout=5 * 1000).chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "How can I list all files in a directory using Python?",
        }
    ],
    model="gpt-3.5-turbo",
)
On timeout, an APITimeoutError is thrown.
Note that requests that time out are retried twice by default.
Advanced
Logging
We use the standard library logging module.
You can enable logging by setting the environment variable OPENAI_LOG to debug.
$ export OPENAI_LOG=debug
How to tell whether None means null or missing
In an API response, a field may be explicitly null, or missing entirely; in either case, its value is None in this library. You can differentiate the two cases with .model_fields_set:
if response.my_field is None:
  if 'my_field' not in response.model_fields_set:
    print('Got json like {}, without a "my_field" key present at all.')
  else:
    print('Got json like {"my_field": null}.')
Accessing raw response data (e.g. headers)
The "raw" Response object can be accessed by prefixing .with_raw_response. to any HTTP method call, e.g.,
from openai import OpenAI

client = OpenAI()
response = client.chat.completions.with_raw_response.create(
    messages=[{
        "role": "user",
        "content": "Say this is a test",
    }],
    model="gpt-3.5-turbo",
)
print(response.headers.get('X-My-Header'))

completion = response.parse()  # get the object that `chat.completions.create()` would have returned
print(completion)
These methods return an LegacyAPIResponse object. This is a legacy class as we're changing it slightly in the next major version.
For the sync client this will mostly be the same with the exception
of content &amp; text will be methods instead of properties. In the
async client, all methods will be async.
A migration script will be provided &amp; the migration in general should
be smooth.
.with_streaming_response
The above interface eagerly reads the full response body when you make the request, which may not always be what you want.
To stream the response body, use .with_streaming_response instead, which requires a context manager and only reads the response body once you call .read(), .text(), .json(), .iter_bytes(), .iter_text(), .iter_lines() or .parse(). In the async client, these are async methods.
As such, .with_streaming_response methods return a different APIResponse object, and the async client returns an AsyncAPIResponse object.
with client.chat.completions.with_streaming_response.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-3.5-turbo",
) as response:
    print(response.headers.get("X-My-Header"))

    for line in response.iter_lines():
        print(line)
The context manager is required so that the response will reliably be closed.
Configuring the HTTP client
You can directly override the httpx client to customize it for your use case, including:

Support for proxies
Custom transports
Additional advanced functionality

import httpx
from openai import OpenAI

client = OpenAI(
    # Or use the `OPENAI_BASE_URL` env var
    base_url="http://my.test.server.example.com:8083",
    http_client=httpx.Client(
        proxies="http://my.test.proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
Managing HTTP resources
By default the library closes underlying HTTP connections whenever the client is garbage collected. You can manually close the client using the .close() method if desired, or with a context manager that closes when exiting.
Microsoft Azure OpenAI
To use this library with Azure OpenAI, use the AzureOpenAI
class instead of the OpenAI class.
ImportantThe Azure API shape differs from the core API shape which means that the static types for responses / params
won't always be correct.

from openai import AzureOpenAI

# gets the API Key from environment variable AZURE_OPENAI_API_KEY
client = AzureOpenAI(
    # https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#rest-api-versioning
    api_version="2023-07-01-preview",
    # https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/create-resource?pivots=web-portal#create-a-resource
    azure_endpoint="https://example-endpoint.openai.azure.com",
)

completion = client.chat.completions.create(
    model="deployment-name",  # e.g. gpt-35-instant
    messages=[
        {
            "role": "user",
            "content": "How do I output all files in a directory using Python?",
        },
    ],
)
print(completion.model_dump_json(indent=2))
In addition to the options provided in the base OpenAI client, the following options are provided:

azure_endpoint (or the AZURE_OPENAI_ENDPOINT environment variable)
azure_deployment
api_version (or the OPENAI_API_VERSION environment variable)
azure_ad_token (or the AZURE_OPENAI_AD_TOKEN environment variable)
azure_ad_token_provider

An example of using the client with Azure Active Directory can be found here.
Versioning
This package generally follows SemVer conventions, though certain backwards-incompatible changes may be released as minor versions:

Changes that only affect static types, without breaking runtime behavior.
Changes to library internals which are technically public but not intended or documented for external use. (Please open a GitHub issue to let us know if you are relying on such internals).
Changes that we do not expect to impact the vast majority of users in practice.

We take backwards-compatibility seriously and work hard to ensure you can rely on a smooth upgrade experience.
We are keen for your feedback; please open an issue with questions, bugs, or suggestions.
Requirements
Python 3.7 or higher.
   

About

        The official Python library for the OpenAI API
      

pypi.org/project/openai/

Topics

  python

  openai

Resources

        Readme
 
License

     Apache-2.0 license
    

Activity
 

Custom properties
 
Stars

18.7k
      stars
 
Watchers

256
      watching
 
Forks

2.5k
      forks
 

          Report repository
 

    Releases
      96

v1.13.2

          Latest
 
Feb 20, 2024

 

        + 95 releases

    Contributors
      105

      + 91 contributors

Languages

Python
99.8%

Other
0.2%

Footer

        © 2024 GitHub,&nbsp;Inc.
      

Footer navigation

Terms

Privacy

Security

Status

Docs

Contact

      Manage cookies
    

      Do not share my personal information
    

    You can’t perform that action at this time.
  