import asyncio


class Foo:
  async def bar(self):
    print("abc")

  def __await__(self):
    return self.bar().__await__()


async def main():
  my_foo = Foo()
  #await my_foo
  loop = asyncio.get_event_loop()
  loop.set_task_factory(task_factory)
  asyncio.create_task(my_foo)


def task_factory(loop, coro):
    if isinstance(coro, Foo):
        return asyncio.Task(coro.bar())

    else:
        return asyncio.Task(coro)


if __name__ == "__main__":
    asyncio.run(main())
