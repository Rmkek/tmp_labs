from flask import Flask, request

app = Flask(__name__)

CHUNK_SIZE = 64


def strip_zeroes(abi_arg):
    for i, _ in enumerate(abi_arg):
        if abi_arg[i] != "0":
            return abi_arg[i:]


# example call:
# http://localhost:5000/parse_abi/?abi=0x4b0bddd200000000000000000000000070997970c51812dc3a010c7d01b50e0d17dc79c80000000000000000000000000000000000000000000000000000000000000001
@app.route("/parse_abi/", methods=["GET"])
def parse_abi():
    # 0x4b0bddd2: method id (keccak256)
    # 00000000000000000000000070997970c51812dc3a010c7d01b50e0d17dc79c8 // 64 bits -- first parameter
    # 0000000000000000000000000000000000000000000000000000000000000001 // 64 bits -- second parameter
    # ... et cetera
    request_abi = request.args.get("abi", "")
    if not request_abi:
        return "No ABI provided, provide with ?abi=...", 401

    try:
        method_id = request_abi[2:10]
        arguments = request_abi[10:]

        argument_list = list(
            map(
                lambda each: strip_zeroes(each),
                [
                    arguments[i : i + CHUNK_SIZE]
                    for i in range(0, len(arguments), CHUNK_SIZE)
                ],
            )
        )
        print(strip_zeroes(argument_list[0]), strip_zeroes(argument_list[1]))

        return {"method_id": method_id, "argument_list": argument_list}
    except:
        return "Wrong ABI encoding, check with https://abi.hashex.org/", 401
