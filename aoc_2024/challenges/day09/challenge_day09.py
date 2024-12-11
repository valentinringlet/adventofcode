import os
from abc import ABCMeta
from dataclasses import dataclass
from enum import Enum, auto

from shared.challenge import Challenge


class BlockType(Enum):
    FREE_SPACE = auto()
    FILE = auto()

    def __invert__(self):
        if self == BlockType.FREE_SPACE:
            return BlockType.FILE
        else:
            return BlockType.FREE_SPACE


@dataclass
class Block(metaclass=ABCMeta):
    type: BlockType
    size: int


@dataclass
class FileBlock(Block):
    id: int


@dataclass
class FreeSpaceBlock(Block):
    pass


class ChallengeDay09(Challenge):
    @classmethod
    def id(cls) -> str:
        return "Day9-not fully solved"

    def _solve(self):
        input_file_name = "test_input_day09.txt"  # "input_day09.txt"  #
        input_file_path = os.path.join(os.path.dirname(__file__), input_file_name)
        blocks = self._parse_input_data(input_file_path)

        # solve part 1
        filesystem_checksum_part1 = 0
        filesystem_idx = 0
        idx_forward = 0
        idx_backward = len(blocks) - 1
        while idx_forward <= idx_backward:
            if blocks[idx_forward].size != 0:
                if blocks[idx_forward].type == BlockType.FILE:
                    filesystem_checksum_part1 += filesystem_idx * blocks[idx_forward].id
                else:  # implicitly: blocks[idx_forward].type == BlockType.FREE_SPACE
                    # skip any free space blocks at the end of the filesystem
                    while blocks[idx_backward].type == BlockType.FREE_SPACE:
                        idx_backward -= 1

                    # add the block id of the last block to the sum
                    filesystem_checksum_part1 += (
                        filesystem_idx * blocks[idx_backward].id
                    )
                    blocks[idx_backward].size -= 1
                    if blocks[idx_backward].size == 0:
                        idx_backward -= 1

                # Move to the next block in the filesystem
                filesystem_idx += 1
                blocks[idx_forward].size -= 1

            if blocks[idx_forward].size == 0:
                idx_forward += 1

        # PROBLEM: answer is too high (6 283 665 299 144)
        self.set_solution(filesystem_checksum_part1, "not solved yet")

    @staticmethod
    def _parse_input_data(file_path: str) -> list[Block]:
        with open(file_path, "r") as file:
            data = [line.strip() for line in file.readlines() if line.strip() != ""][0]

        blocks = []
        curr_block_type = BlockType.FILE
        curr_file_id = 0
        for char in data:
            if curr_block_type == BlockType.FILE:
                curr_block = FileBlock(
                    type=curr_block_type, size=int(char), id=curr_file_id
                )
                curr_file_id += 1
            else:
                curr_block = FreeSpaceBlock(type=curr_block_type, size=int(char))
            blocks.append(curr_block)
            curr_block_type = ~curr_block_type

        return blocks
