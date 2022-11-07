#pragma once

#include <cstddef>
#include <cstdint>

using u8   = std::uint8_t;
using u16  = std::uint16_t;
using u32  = std::uint32_t;
using u64  = std::uint64_t;
using u128 = __uint128_t;

using i8   = std::int8_t;
using i16  = std::int16_t;
using i32  = std::int32_t;
using i64  = std::int64_t;
using i128 = __int128_t;

using color_t = u32;

namespace hex {

    struct Region {
        u64 address;
        size_t size;

        [[nodiscard]] bool isWithin(const Region &other) const;
        [[nodiscard]] bool overlaps(const Region &other) const;

        [[nodiscard]] u64 getStartAddress() const;
        [[nodiscard]] u64 getEndAddress() const;
        [[nodiscard]] size_t getSize() const;

        bool operator==(const Region &other) const;

        constexpr static Region Invalid() {
            return { 0, 0 };
        }
    };

}