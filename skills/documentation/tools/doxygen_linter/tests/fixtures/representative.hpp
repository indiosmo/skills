/** @file representative.hpp */

const char *literal = "/** @brief Not documentation */";
const char *raw_literal = R"doc(/** @param fake invalid */)doc";

/**
 * @brief Read a value.
 * @param [in] count Number of values.
 * @return The value.
 */
int read(int count);

/**
 * @brief Read a value.
 * @param [in] count Number of values.
 * @return The value.
 */
double read(double count);

/**
 * @brief Store values.
 * @tparam Value The value type.
 */
template<typename Value>
struct Store {
    /**
     * @brief Visit stored values.
     * @param [in] visitor Function called for each value.
     * @par Returns
     * Nothing.
     */
    void visit(void (*visitor)(Value value));
};

#define DECLARE_READER(name) int name(int count)
/** @brief Read values through the configured adapter. */
DECLARE_READER(adapter_read);

/**
 * @details
 * Read the requested value.
 */
int read(int count) { return count; }
