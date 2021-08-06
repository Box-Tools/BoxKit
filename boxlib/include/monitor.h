#ifndef UTILITIES_MONITOR_H
#define UTILITIES_MONITOR_H

#include <indicators/block_progress_bar.hpp>
#include <indicators/progress_bar.hpp>

using namespace indicators;

namespace bubblebox::utilities
{
    class Monitor
    {
    public:
        // default destructor
        ~Monitor()                             = default;

        // delete everything else
        Monitor           (Monitor const&) = delete;
        Monitor& operator=(Monitor const&) = delete;
        Monitor           (Monitor&&)      = delete;
        Monitor& operator=(Monitor&&)      = delete;

        // constructors
        Monitor(int _numIter);

        // methods
        void update();
        void finish();

    private:
        int progress;
        int numIter;

        /*
        BlockProgressBar bar {option::BarWidth{50}, option::ForegroundColor{Color::cyan},
                              option::FontStyles{std::vector<FontStyle>{FontStyle::bold}},
                              option::MaxProgress{numIter}};
        */

        ProgressBar bar{option::BarWidth{50},
                        option::Start{"["},
                        option::Fill{"="},
                        option::Lead{">"},
                        option::Remainder{" "},
                        option::End{" ]"},
                        option::ShowPercentage{true},
                        option::MaxProgress{numIter},
                        option::ForegroundColor{Color::green},
                        option::FontStyles{std::vector<FontStyle>{FontStyle::bold}}};

    };
}
#endif
