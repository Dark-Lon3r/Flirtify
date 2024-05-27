from aiogram.types import CallbackQuery, Message, LabeledPrice, PreCheckoutQuery, ShippingOption, ShippingQuery, ContentType
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.types import Location
from geopy.geocoders import Nominatim
from functools import lru_cache, cache
from utils.set_bot_commands import set_default_commands

import json
import os
import logging
import asyncio
import sqlite3
import aiosqlite
import aiohttp
import multiprocessing
import threading