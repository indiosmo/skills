#include "gain.hpp"
#include <iostream>

int main() {
    //! [scale_sample]
    const float sample = 0.25F;
    const float gain = 2.0F;
    const float wet_signal = apply_gain(sample, gain);
    //! [scale_sample]
    std::cout << wet_signal << '\n';
    return wet_signal == 0.5F ? 0 : 1;
}
