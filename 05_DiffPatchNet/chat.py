import asyncio
import cowsay

clients = {}
available_cows = cowsay.list_cows()


async def who(writer) -> None:
    writer.write(f"Registered users: {', '.join(clients.keys())}\n".encode())
    await writer.drain()


async def cows(writer) -> None:
    writer.write(f"Available cows: {', '.join(cowsay.list_cows())}\n".encode())
    await writer.drain()


async def login(is_reg, name, writer, receive) -> tuple[bool, str]:
    me = None
    if name in available_cows:
        me = name
        print("Registered: ", me)
        clients[me] = asyncio.Queue()
        available_cows.remove(name)
        writer.write("Registration succeed.\n".encode())
        await writer.drain()
        is_reg = True
        receive.cancel()
        asyncio.create_task(clients[me].get())
    else:
        writer.write("Wrong name.\n".encode())
        await writer.drain()
    return is_reg, me


async def say(user, me, writer, text) -> None:
    if user in clients.keys():
        await clients[user].put(f"From: {me}\n {cowsay.cowsay((' '.join(text)).strip(), cow=me)}")
        writer.write("Message successfully send.\n".encode())
        await writer.drain()
    else:
        writer.write(f"User with name {user} not found.\n".encode())
        await writer.drain()


async def yield_cow(me, writer, text) -> None:
    for out in clients.values():
        if out is not clients[me]:
            await out.put(f"From: {me}\n {cowsay.cowsay(' '.join(text).strip(), cow=me)}")
    writer.write("Message successfully send.\n".encode())
    await writer.drain()


async def quit(receive, send, is_reg, me, writer) -> None:
    receive.cancel()
    send.cancel()
    if is_reg:
        del clients[me]
        print("Quited: ", me)
        available_cows.append(me)
    writer.close()
    await writer.wait_closed()


async def chat(reader, writer):
    me = ""
    is_reg = False
    is_quit = False

    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())

    while not reader.at_eof() and not is_quit:
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)

        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                message = q.result().decode().split()

                if len(message) < 1:
                    continue
                elif message[0] == "who":
                    await who(writer)
                elif message[0] == 'cows':
                    await cows(writer)
                elif message[0] == "login" and message[1] in available_cows:
                    name = message[1]
                    if not is_reg:
                        is_reg, me = login(is_reg, name, writer, receive)
                elif message[0] == "say":
                    user = message[1]
                    text = message[2]
                    if is_reg:
                        await say(user, me, writer, text)
                    else:
                        writer.write("You need log in to start chatting.\n".encode())
                        await writer.drain()
                        continue
                elif message == "yield":
                    text = message[1]
                    if is_reg:
                        await yield_cow(me, writer, text)
                    else:
                        writer.write("You need log in to start chatting.\n".encode())
                        await writer.drain()
                        continue
                elif message == "quit":
                    await quit(receive, send, is_reg, me, writer)
                    is_quit = True
                    break
                else:
                    writer.write("Unknown command.\n".encode())
                    await writer.drain()
                    continue
            elif q is receive and is_reg:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    print("Quited: ", me)
    del clients[me]
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
