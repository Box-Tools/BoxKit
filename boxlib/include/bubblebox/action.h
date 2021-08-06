#ifndef BUBBLEBOX_ACTION_H
#define BUBBLEBOX_ACTION_H

#include <bubblebox/pytypes.hpp>
#include <indicators/progress_bar.hpp>

using namespace bubblebox::pytypes;

namespace bubblebox::utilities
{

    class Action: public CPyObject
    {
    public:

        //constructors
	Action() {}
	Action(PyObject* _pyObject);

        //destructors
	virtual ~Action() {}

        //attributes
        int nthreads;
        bool monitor;
        PyObject* target;

        //methods
        void setbar(int iterlimit);
        void updatebar();

    private:

        //private attributes
        int max_progress;
        int progress;

        indicators::ProgressBar bar{indicators::option::BarWidth{50},
                                    indicators::option::Start{"["},
                                    indicators::option::Fill{"="},
                                    indicators::option::Lead{">"},
                                    indicators::option::Remainder{" "},
                                    indicators::option::End{" ]"},
                                    indicators::option::ShowPercentage{true},
                                    indicators::option::ForegroundColor{indicators::Color::green},
                                    indicators::option::FontStyles{std::vector<indicators::FontStyle>
                                                                       {indicators::FontStyle::bold}}};



    };

}
#endif
