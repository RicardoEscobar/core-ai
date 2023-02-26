# Core AI

A rare and valuable independent AI core. This is the physical soul of an artificial intelligence, an artifact of astounding complexity capable of sophisticated thought exceeding the human mind. An object of fear, worship, and avarice.

# Legal

Possession and sale of AI cores is banned by __REDACTED__, __REDACTED__, __REDACTED__, __REDACTED__, __REDACTED__ and __REDACTED__, and they may be seized as contraband if found by __REDACTED__ inspections. However, they can be turned in directly by talking to __REDACTED__ of any __REDACTED__ except the __REDACTED__, providing various ratios of __REDACTED__.

Alternatively, they can also be used to augment __REDACTED__ and __REDACTED__ on __REDACTED__. Use of AI cores on a __REDACTED__ may trigger __REDACTED__ inspections and attract the attention of the __REDACTED__. Higher-level cores are worth more, have better effects, and attract more __REDACTED__ and __REDACTED__ attention.

# Types

## Gamma Core

A gamma-level AI core is capable of supporting most human endeavors, making up for a lack of creativity and problem-solving ability with prodigous computational prowess. Assigning a gamma to aid human overseers in administering an industry brings significant benefits.

A rare and valuable independent AI core, the gamma-level is the lowest tier core considered to be truly intelligent under AI protocols. A gamma core will employ remarkable judgment and reasoning when assigned to straightforward tasks while using its savant-like data processing abilities to far exceed any individual human's abilities. It is relatively uncreative in problem-solving however, preferring to fall back upon direct, unsophisticated means.

## Beta Core

A beta-level AI core is capable of ably supporting most human endeavors, matching not-quite-human performance with its prodigous computational ability. Assigning a beta to aid humans in administering an industry brings significant benefits.

A beta-level AI core can easily pass for human, given anonymized communications protocols, and will readily and ably lie if deception is required to perform a given task. The beta employs cognitive modelling of human actors to anticipate reactions and emotional responses, though it is difficult to describe exactly what, if anything, the beta feels. A beta will model a new personality for each human it comes into contact with.

## Alpha Core

An alpha-level AI core is capable of excelling at any task. Assigning one to run an industry brings benefits well beyond the capacity of human leadership, and there are even rumors of alpha cores surreptitiously assigned to govern entire __REDACTED__.

The alpha-level AI core is the physical soul of a fearsome intelligence. An alpha can create art which perfectly simulates human pathos, plausibly debate any philosophical position, and form what appear to be deep and meaningful bonds with human beings. Alphas have been known to perform elaborate 'jokes' built over years which can only be appreciated due to the intention that a particular human subject become cognitive of the whole at a specific time and context.

Although the locus of vast material and intellectual investment, alphas terrified __REDACTED__ or any industry domain strategic planners. Like all AI, each alpha was watched, controlled, and ruthlessly eliminated at the first sign of disloyalty. The __REDACTED__ carries on these policies with even greater fervor.

# Create virtual environment

After cloning the repository, (if you are reading this, you probably already did) you need to create a vitual environment for installing the requirements.

```shell
python -m venv venv
```

This process takes around ttwo minutes.

# Install requirements

To work with the project you need to install modules to conect to the database and load environment variables.

## psycopg 3

This module connects __Python__ scripts to a __PostgreSQL__ database, here is where I'm storing AI model data.

Go to [this link](https://www.psycopg.org/psycopg3/docs/basic/install.html) to check details on __psycopg 3__ installation.

```shell
pip install --upgrade pip           # upgrade pip to at least 20.3
```

## python-dotenv

Python-dotenv reads key-value pairs from a .env file and can set them as environment variables. I use this to connect to a database and hiding the connection info from others.

```shell
pip install python-dotenv
```