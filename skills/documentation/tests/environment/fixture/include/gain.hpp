/** @file gain.hpp
 * @brief Audio gain operations.
 */

/** @brief Scale a sample by a gain factor.
 * @param sample Input sample amplitude.
 * @param gain Linear gain factor.
 * @return Scaled sample amplitude.
 * @see apply_gain(float)
 * @snippet gain.cpp scale_sample
 */
inline float apply_gain(float sample, float gain) { return sample * gain; }

/** @brief Scale a sample by the default gain of two.
 * @param sample Input sample amplitude.
 * @return Scaled sample amplitude.
 * @see apply_gain(float, float)
 */
inline float apply_gain(float sample) { return apply_gain(sample, 2.0F); }
