# Sal-Puppet

This image comprises of a Puppet Server that uses Sal to validate certificate signing requests. See the end of the readme for a example ``csr_attributes.yaml``.

## Usage

This image extends (grahamgilbet/puppetserver)[https://registry.hub.docker.com/u/grahamgilbert/puppetserver/]. For full usage instructions for that image, see it's repository.

## Environment variables

* ``SAL_PUPPETSERVER_URL``: The URL of your Sal server. Defaults to ``http://sal``
* ``SAL_PUPPETSERVER_PRIVATE_KEY``: Your Sal API Private Key. Defaults to ``123``
* ``SAL_PUPPETSERVER_PUBLIC_KEY``: Your Sal API Public Key. Defaults to ``123``
