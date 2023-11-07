#!/bin/bash

git pull

cd front
npm run build

service apache2 restart